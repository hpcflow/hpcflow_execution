from types import NoneType
from paramiko import SSHClient, Transport, AutoAddPolicy
import scp

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
        self.client_scp = NoneType

def connection(self):

    self.client_ssh = ssh_connection(self.user, self.host)
    self.client_scp = scp_connection(self.client_ssh)


def ssh_connection(uname, host):

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    ssh._transport = Transport(host)
    ssh._transport.connect()
    ssh._transport.auth_interactive_dumb(username=uname, handler=None)

    return ssh

def scp_connection(ssh):

    scp = scp.SCPClient(ssh.get_transport())

    return scp

def execute_command_ssh(self, command):

    stdin, stdout, stderr = self.ssh_client.exec_command(command)

    return stdin, stdout, stderr
