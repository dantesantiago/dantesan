# 2019 - Cigent Technology, Inc.
#      - MSP D3E Subscription: ssh/DB utilities
# by dantesan


import subprocess
HOST = "dsantiago@10.200.50.205"

def run_command(command):
    ssh = subprocess.Popen(["ssh", "%s" % HOST, command],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    return(result)
