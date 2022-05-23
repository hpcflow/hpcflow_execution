from multiprocessing.sharedctypes import Value
import sched
import subprocess
import sunau
import sys
from typing import Type
import secrets
from pathlib import Path

from src import scriptgen

#   commands = [
#       [ # commands for task 1
#           "doSomething parameter1 parameter2",
#           "doSomethingElse parameter1"
#       ],
#       [
#           # commands for task 2
#       ],
#       ...
#   ]

# commands is list of lists where each lower level list contains strings which are commands to be executed.



def run_elements(commands, scheduler='direct'):

    # Folder will need more descriptive name in future, ideally using name of workflow. Could consider shorter hex
    # or even just sequential numbering?
    workflow_id = f'{commands[0]}_{secrets.token_hex(10)}'
    base_folder = Path.cwd()
    workflow_path = create_workflow_path(workflow_id, base_folder)

    platform_string = sys.platform
    # host_os should return 'linux' for Linux, 'darwin' for macOS, 'cygwin' for windows/cygwin, 'win32' for windows.
    # assume WSL returns 'linux', powershell returns 'win32' and cmd.exe returns 'win32'.
    # Will want to change this later when running on multiple systems? Or use this to check what current matflow 
    # instance is running on?

    if platform_string in ['linux', 'darwin', 'cygwin']:
        host_os = 'posix'
    elif platform_string in ['win32']:
        host_os = 'windows'

    to_run = [scriptgen.write_execution_files(command, command_idx, scheduler, host_os, workflow_path) 
        for command_idx, command in enumerate(commands[1:])]
    
    for command in to_run:
        command_info = subprocess.run(command, shell=True, cwd=workflow_path)
        command_info.check_returncode()


def create_workflow_path(workflow_id, base_folder):

    workflow_path = base_folder / workflow_id

    workflow_path.mkdir()

    return workflow_path
