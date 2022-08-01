import collections
import subprocess
import secrets
from pathlib import Path

from hpcflow_execution import scriptgen
from hpcflow_execution import RemoteClient

def run_elements(workflow_dict):

    # Create local folder

    workflow_id = f'{workflow_dict["name"]}_{secrets.token_hex(10)}'
    base_folder = Path.cwd()
    workflow_path = create_workflow_path(workflow_id, base_folder)

    # Write script files to local folder and return list containing filenames 
    # and command to initiate each task.

    print(f'Writing scripts and job submission files.')
    to_run = [
        scriptgen.write_execution_files(task, task_idx, workflow_path) 
            for task_idx, task in enumerate(workflow_dict["tasks"])
            ]

    # Create workflow folder on each remote resource and copy relevant files 
    # for each task.

    remote_prep_done = set()
    remote_folders = collections.defaultdict(list)
    remote_clients = collections.defaultdict(None)
    scp_out = []

    for num, task in enumerate(workflow_dict["tasks"]):

        if task['location'] == 'remote':
            
            if task['hostname'] not in remote_prep_done:

                remote_clients[task['hostname']] = RemoteClient.RemoteClient(
                    task['hostname'], task['username'], task['basefolder']
                    )
                remote_folders[task['hostname']] = create_remote_workflow_path(
                    workflow_id, remote_clients[task['hostname']]
                    )
                remote_prep_done.add(task['hostname'])

            remote_clients[task['hostname']].bulk_upload(
                remote_folders[task['hostname']], to_run[num][1:][0]
                ) 

    # Now execute each task
    # NB For remote, queued tasks they are all getting submitted to the 
    # queueing software one after the other. This will need to be dealt with 
    # to avoid dependency problems.

    for num, task in enumerate(workflow_dict["tasks"]):

        if task['location'] == 'local':
            
            command_info = subprocess.run(
                to_run[num][0], shell=True, cwd=workflow_path
                )
            command_info.check_returncode()

        elif task['location'] == 'remote':

            remote_clients[task['hostname']].execute_commands(
                remote_clients[task['hostname']].remote_path, [to_run[num][0]]
                )

    return to_run, scp_out


def create_workflow_path(workflow_id, base_folder):

    workflow_path = base_folder / workflow_id

    print(f'Creating local workflow folder at {workflow_path}...')

    workflow_path.mkdir()

    print(f'Complete\n')

    return workflow_path


def create_remote_workflow_path(workflow_id, RemoteClient):

    remote_workflow_path = Path(RemoteClient.remote_path) / Path(workflow_id)

    print(f'Creating remote workflow folder at \
        {RemoteClient.host}:{remote_workflow_path}...')

    RemoteClient.execute_commands(
        Path(RemoteClient.remote_path), [f'mkdir {remote_workflow_path}']
        )

    print(f'Complete\n')

    return remote_workflow_path
