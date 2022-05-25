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

def scp_to_remote_with_sp(username, hostname, files, dest):

    scp = subprocess.Popen(["scp", "%s" % files, f"{username}@{hostname}:{dest}"],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

    return scp

#   result = scp.stdout.readlines()

#    if result == []:
#
#        error = scp.stderr.readlines()
#        print >>sys.stderr, "ERROR: %s" % error

#    else:

#        print(result)

def scp_from_remote_with_sp(username, hostname, files, dest):

    scp = subprocess.Popen(["scp", "%s" % f"{username}@{hostname}:{files}", dest],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

    #result = scp.stdout.readlines()

    #if result == []:
    #
    #    error = scp.stderr.readlines()
    #    print >>sys.stderr, "ERROR: %s" % error

    #else:

    #    print(result)