from multiprocessing import AuthenticationError
from types import NoneType
from paramiko import SSHClient, Transport, AutoAddPolicy
import scp
import logging

class RemoteClient:

    def __init__(
        self,
        host: str,
        user: str,
        remote_path: str,

    ):
        self.host = host
        self.user = user
        self.remote_path = remote_path

        self.client_ssh = None
        self.client_scp = None

        self.logger = self.logger_setup()


def logger_setup():
        logger = logging.getLogger(__name__)

        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('file.log')
        c_handler.setLevel(logging.WARNING)
        f_handler.setLevel(logging.ERROR)

        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        return logger


@property
def connection(self):

    self.client_ssh = ssh_connection(self.user, self.host)
    self.client_scp = scp_connection(self.client_ssh)


@connection.deleter
def connection(self):

    self.client_ssh.close()
    self.client_scp.close()


def ssh_connection(self, uname, host):

    try:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())

        ssh._transport = Transport(host)
        ssh._transport.connect()
        ssh._transport.auth_interactive_dumb(username=uname, handler=None)

        return ssh
    except AuthenticationException as e:
        self.logger.error(
            f"AuthenticationException occurred: {e}"
            )
    except Exception as e:
        self.logger.error(
            f"Unexpected error occurred while connecting to host: {e}"
        )


def scp_connection(self, ssh):

    scp = scp.SCPClient(ssh.get_transport())

    return scp


def execute_commands(self, commands: list[str]):

    """
    Execute multiple commands in succession.

    :param List[str] dommands: List of unix commands as strings.
    """

    for cmd in commands:
        stdin, stdout, stderr = self.connection.exec_command(cmd)
        stdout.channel.recv_exit_status()
        response = stdout.readlines()
        for line in response:
            self.logger.info(
                f"INPUT: {cmd}\n \
                OUTPUT: {line}"
            )

def bulk_upload(self, filepaths: list[str]):

    try:
        self.scp.put(
            filepaths,
            remote_path = self.remote_path,
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
    self.scp.get(file)