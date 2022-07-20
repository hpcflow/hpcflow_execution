from typing import List

from paramiko import AutoAddPolicy, SSHClient, Transport
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException
from pathlib import Path

import logging

import getpass

class RemoteClient:

    def __init__(
        self,
        host: str,
        user: str,
        remote_path: str,

    ):
        self.host = host
        self.user = user
        self.remote_path = Path(remote_path)

        self._ssh_client = None
        self._scp_client = None

        self.logger = self.logger_setup()

    def __repr__(self):
        return f'RemoteClient({self.host}, {self.user}, {self.remote_path})'

    @property
    def ssh_client(self):

        def handler(title, instructions, prompt_list):
            answers = []
            for prompt_,_ in prompt_list:
                prompt = prompt_.strip().lower()
                if prompt.startswith('password'):
                    answers.append(getpass.getpass())
                else:
                    raise ValueError('Unknown prompt: {}'.format(prompt_))
            return answers

        if self._ssh_client is None:

            try:
                ssh_client = SSHClient()
                ssh_client.set_missing_host_key_policy(AutoAddPolicy())

                ssh_client._transport = Transport(self.host)
                ssh_client._transport.connect()
        #        ssh_client._transport.auth_interactive_dumb(username=self.user, handler=None)
                ssh_client._transport.auth_interactive(self.user, handler)

                self._ssh_client = ssh_client

                return self._ssh_client

            except AuthenticationException as e:
                self.logger.error(
                    f"AuthenticationException occurred: {e}"
                    )

            except Exception as e:
                self.logger.error(
                    f"Unexpected error occurred while connecting to host: {e}"
                )
        else:

            return self._ssh_client

    @ssh_client.deleter
    def ssh_client(self):

        self._ssh_client.close()
        self._ssh_client = None

    @property
    def scp_client(self):

        if self._scp_client is None:

            ssh_cl = self.ssh_client
            scp_client = SCPClient(ssh_cl.get_transport())

            self._scp_client = scp_client

            return self._scp_client

        else:

            return self._scp_client

    @scp_client.deleter
    def scp_client(self):

        self._scp_client.close()
        self._scp_client = None

    def logger_setup(self):
        
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('file.log')
        #c_handler.setLevel(logging.INFO)
        #f_handler.setLevel(logging.INFO)

        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        return logger

    def execute_commands(self, exec_folder, commands: List[str]):

        """
        Execute multiple commands in succession.

        :param List[str] dommands: List of unix commands as strings.
        """

        for cmd in commands:

            try:
                stdin, stdout, stderr = self.ssh_client.exec_command(f"cd {exec_folder} && {cmd}")
                stdout.channel.recv_exit_status()
                response = stdout.readlines()

                for line in response:
                    self.logger.info(
                        f"INPUT: {cmd}\n \
                        OUTPUT: {line}"
                    )
            except SSHException as e:
                self.logger.error(f"SSHException while executing command remotely: {e}")

    def bulk_upload(self, upload_folder, filepaths: List[str]):

        try:
            self.scp_client.put(
                filepaths,
                remote_path = self.remote_path / upload_folder ,
                recursive = True
            )
            self.logger.info(
                f"Finished uploading {len(filepaths)} files to {self.remote_path} on {self.host}"
            )
        except SCPException as e:
            self.logger.error(
                f"SCPException during bulk upload: {e}"
            )
        except Exception as e:
            self.logger.error(
                f"Unexpected exception during bulk upload: {e}"
            )

    def download_file(self, file: str):
        """Download file from remote host."""
        self.scp_client.get(file)