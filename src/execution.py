from multiprocessing.sharedctypes import Value
import sched
import subprocess
import sunau
import sys
from typing import Type
import secrets
from pathlib import Path

from src import scriptgen

def run_elements(commands, scheduler='direct'):

    workflow_id = secrets.token_hex(10)
    #base_folder = Path.cwd()
    base_folder = Path('')

    workflow_path = create_workflow_path(workflow_id, base_folder)

    platform_string = sys.platform

    # host_os should return 'linux' for Linux, 'darwin' for macOS, 'cygwin' for windows/cygwin, 'win32' for windows.
    # assume WSL returns 'linux', powershell returns 'win32' and cmd.exe returns 'win32'

    if platform_string in ['linux', 'darwin', 'cygwin']:
        host_os = 'posix'
    elif platform_string in ['win32']:
        host_os = 'windows'

    to_run = [scriptgen.write_execution_files(command, command_idx, scheduler, host_os, workflow_path) for command_idx, command in 
        enumerate(commands)]
    
    for command in to_run:
        command_info = subprocess.run(command, shell=True, cwd=workflow_path)
        command_info.check_returncode()


def create_workflow_path(workflow_id, base_folder):

    workflow_path = base_folder / workflow_id

    workflow_path.mkdir()

    return workflow_path
