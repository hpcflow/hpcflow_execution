import collections
from multiprocessing.sharedctypes import Value
import sched
import subprocess
import sunau
import sys
from typing import Type
import secrets
from pathlib import Path

from hpcflow_execution import scriptgen
from hpcflow_execution import remote_with_sp

from hpcflow_execution import RemoteClient

def run_elements(commands):

    # Create local folder

    workflow_id = f'{commands[0]}_{secrets.token_hex(10)}'
    base_folder = Path.cwd()
    workflow_path = create_workflow_path(workflow_id, base_folder)

    # Write script files to local folder and return list containing filenames and command to initiate each task.

    to_run = [
        scriptgen.write_execution_files(task['command'], task_idx, task['scheduler'], task['host_os'], workflow_path) 
        for task_idx, task in enumerate(commands[1:])
        ]

    # Create workflow folder on each remote resource and copy relevant files for each task.

    remote_prep_done = set()
    remote_folders = collections.defaultdict(list)
    remote_clients = collections.defaultdict(None)
    scp_out = []

    for num, task in enumerate(commands[1:]):

        if task['location'] == 'remote':
            
            if task['hostname'] not in remote_prep_done:

                remote_clients[task['hostname']] = RemoteClient.RemoteClient(task['hostname'], task['username'], task['basefolder'])
                remote_folders[task['hostname']] = create_remote_workflow_path(workflow_id, remote_clients[task['hostname']])
                remote_prep_done.add(task['hostname'])

            remote_clients[task['hostname']].bulk_upload(remote_folders[task['hostname']], to_run[num][1:][0]) 

    # Now execute each task
    # NB For remote, queued tasks they are all getting submitted to the queueing software one after the other. This
    # will need to be dealt with to avoid dependency problems.

    for num, task in enumerate(commands[1:]):

        if task['location'] == 'local':
            
            command_info = subprocess.run(to_run[num][0], shell=True, cwd=workflow_path)
            command_info.check_returncode()

        elif task['location'] == 'remote':

            #remote_clients[task['hostname']].execute_commands(remote_folders[task['hostname']], [to_run[num][0]])
            remote_clients[task['hostname']].execute_commands(remote_clients[task['hostname']].remote_path, [to_run[num][0]])


    return to_run, scp_out

def run_elements_old(commands, scheduler='direct'):

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

    print(f'Creating local workflow folder at {workflow_path}...')

    workflow_path.mkdir()

    print(f'Complete\n')

    return workflow_path

def create_remote_workflow_path(workflow_id, RemoteClient):

    remote_workflow_path = Path(RemoteClient.remote_path) / Path(workflow_id)

    print(f'Creating remote workflow folder at {RemoteClient.host}:{remote_workflow_path}...')

    RemoteClient.execute_commands(Path(RemoteClient.remote_path), [f'mkdir {remote_workflow_path}'])

    print(f'Complete\n')

    return remote_workflow_path
