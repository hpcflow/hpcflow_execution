import paramiko

def ssh_connect(uname, host):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh._transport = paramiko.Transport(host)
    ssh._transport.connect()
    ssh._transport.auth_interactive_dumb(username=uname, handler=None)

    return ssh

def execute_command_ssh(ssh, command)

    stdin, stdout, stderr = ssh.exec_command(command)

    return stdin, stdout, stderr
