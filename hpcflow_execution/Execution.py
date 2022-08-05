import collections
import subprocess
import secrets
import json
from pathlib import Path

from hpcflow_execution import file_handler
from hpcflow_execution import RemoteClient

class Execution:

    def __init__(
        self
    ):
        self.remote_clients = collections.defaultdict(None)
        self.remote_prep_done = set()


    def prep_workflow(self, workflow_json):
    
        workflow_dict = json.loads(workflow_json)

        workflow_id = f'{workflow_dict["name"]}_{secrets.token_hex(10)}'

        workflow_persistant = file_handler.create_persistant_workflow(
            workflow_id, 
           workflow_dict
            )

        return workflow_persistant


    def prep_tasks(self, workflow_persistant):

        # Write script files to local folder and return list containing filenames 
        # and command to initiate each task.

        print(f'Writing scripts and job submission files.')

        for task_idx, task in enumerate(workflow_persistant.attrs["tasks"]):

            if workflow_persistant.attrs["tasks"][task_idx]["status"] == 0:

                workflow_persistant = file_handler.write_execution_files(
                    task, task_idx, workflow_persistant)

                if task['location'] == 'remote':
            
                    if task['hostname'] not in self.remote_prep_done:

                        self.remote_clients[task['hostname']] = RemoteClient.RemoteClient(
                                task['hostname'], task['username'], task['basefolder']
                                )

                        self.remote_prep_done.add(task['hostname'])

                workflow_persistant.attrs["tasks"][task_idx]["status"] = 1

        return workflow_persistant
                
        # Now execute each task
        # NB For remote, queued tasks they are all getting submitted to the 
        # queueing software one after the other. This will need to be dealt with 
        # to avoid dependency problems.

    def run_tasks(self, workflow_persistant, location):

        for task_idx, task in enumerate(workflow_persistant.attrs["tasks"]):

            if task["location"] == "local" and location == "local":
            
                command_info = subprocess.run(
                    task["execute"], shell=True, cwd=task["exec_dir"]
                    )
                command_info.check_returncode()

            elif task['location'] == 'remote' and "location" "local":

                self.remote_clients[task['hostname']].execute_commands(
                    self.remote_clients[task['hostname']].remote_path, 
                    [to_run[task_idx][0]]
                )

            workflow_persistant.attrs["tasks"][task_idx]["status"] = 2


        return workflow_persistant