import subprocess
import sys

def ssh_with_sp(username, hostname, command):

    ssh = subprocess.Popen(["ssh", "%s" % f"{username}@{hostname}", command],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

    result = ssh.stdout.readlines()

    if result == []:

        error = ssh.stderr.readlines()
        print >>sys.stderr, "ERROR: %s" % error

    else:

        print(result)