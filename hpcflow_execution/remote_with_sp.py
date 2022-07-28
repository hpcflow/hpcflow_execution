import subprocess
import sys

ssh_return_codes = {
    0 : 'Operation was successful',
    1 : 'Generic error, usually because invalid command line options or malformed configuration',
    2 : 'Connection failed',
    65 : 'Host not allowed to connect',
    66 : 'General error in ssh protocol',
    67 : 'Key exchange failed',
    68 : 'Reserved',
    69 : 'MAC error',
    70 : 'Compression error',
    71 : 'Service not available',
    72 : 'Protocol version not supported',
    73 : 'Host key not verifiable',
    74 : 'Connection failed',
    75 : 'Disconnected by application',
    76 : 'Too many connections',
    77 : 'Authentication cancelled by user',
    78 : 'No more authentication methods available',
    79 : 'Invalid user name',
    127: 'BASH: Command not found'
}

scp_return_codes = {
    0 : 'Operation was successful',
    1 : 'General error in file copy',
    2 : 'Destination is not directory, but it should be',
    3 : 'Maximum symlink level exceeded',
    4 : 'Connecting to host failed',
    5 : 'Connection broken',
    6 : 'File does not exist',
    7 : 'No permission to access file.',
    8 : 'General error in sftp protocol',
    9 : 'File transfer protocol mismatch',
    10 : 'No file matches a given criteria',
    65 : 'Host not allowed to connect',
    66 : 'General error in ssh protocol',
    67 : 'Key exchange failed',
    68 : 'Reserved',
    69 : 'MAC error',
    70 : 'Compression error',
    71 : 'Service not available',
    72 : 'Protocol version not supported',
    73 : 'Host key not verifiable',
    74 : 'Connection failed',
    75 : 'Disconnected by application',
    76 : 'Too many connections',
    77 : 'Authentication cancelled by user',
    78 : 'No more authentication methods available',
    79 : 'Invalid user name'

}

def ssh_with_sp(username, hostname, command, local_directory, remote_directory):

    print(f'Executing command:\n\t{command}')

    ssh_out = subprocess.Popen(["ssh", "%s" % f"{username}@{hostname}", f"cd {remote_directory} && {command}"],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       cwd=local_directory)
    ssh_out.wait()

    assert ssh_out.returncode == 0, f"ssh failed with return code {ssh_out.returncode}: {ssh_return_codes[ssh_out.returncode]}"

    return ssh_out

def scp_to_remote_with_sp(username, hostname, file_list, dest):

    files = ', '.join(file_list)

    print(f'Copying file(s) to remote folder {hostname}:{dest}:\n{files}')

    scp_out = subprocess.Popen(["scp", *file_list, f"{username}@{hostname}:{dest}"],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

    scp_out.wait()

    print(f'Complete')

    assert scp_out.returncode == 0, f"scp to remote failed with return code {scp_out.returncode}: {scp_return_codes[scp_out.returncode]}"

    return scp_out

def scp_from_remote_with_sp(username, hostname, files, dest):

    scp_out = subprocess.Popen(["scp", "%s" % f"{username}@{hostname}:{files}", dest],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

    scp_out.wait()

    assert scp_out.returncode == 0, f"scp from remote failed with return code {scp_out.returncode}: {scp_return_codes[scp_out.returncode]}"

    return scp_out