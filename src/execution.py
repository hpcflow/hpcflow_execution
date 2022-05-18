from multiprocessing.sharedctypes import Value
import sched
import subprocess
import sunau
import sys
from typing import Type

from src import scriptgen

def run_elements(commands, scheduler='direct'):

    platform_string = sys.platform

    # host_os should return 'linux' for Linux, 'darwin' for macOS, 'cygwin' for windows/cygwin, 'win32' for windows.
    # assume WSL returns 'linux', powershell returns 'win32' and cmd.exe returns 'win32'

    if platform_string in ['linux', 'darwin', 'cygwin']:
        host_os = 'posix'
    elif platform_string in ['win32']:
        host_os = 'windows'

    to_run = [scriptgen.write_execution_files(command, command_idx, scheduler, host_os) for command_idx, command in 
        enumerate(commands)]
    
    for command in to_run:
        command_info = subprocess.run(command, shell=True)
        command_info.check_returncode()
#