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
            

    def run_tasks(self, workflow_persistant, location):

        for task_idx, task in enumerate(workflow_persistant.attrs["tasks"]):

            current_status = workflow_persistant.attrs["tasks"][task_idx]["status"]

            if task["location"] == "local" and location == "local" and current_status == 1:
            
                command_info = subprocess.run(
                    task["execute"], shell=True, cwd=task["exec_dir"]
                    )
                command_info.check_returncode()

                status_update = 2

            elif task["location"] == "remote" and location == "remote" and current_status == 1:

                command_info = subprocess.run(
                    task["execute"], shell=True, cwd=task["exec_dir"]
                    )

                command_info.check_returncode()

                status_update = 2

            elif task['location'] == "remote" and location == "local" and current_status == 1:

              self.handover_local_to_remote(task_idx, workflow_persistant)
              status_update = 1

            
            elif task['location'] == "local" and location == "remote" and current_status == 1:

              self.handover_remote_to_local()
              status_update = 1
              
            else:
            
                raise Exception('Lost while running tasks!')
            
            workflow_persistant.attrs["tasks"][task_idx]["status"] = status_update


        return workflow_persistant


    def handover_local_to_remote(self, task_idx, workflow_persistant):

        print(f'Handing over to remote...')
        print(self.remote_clients)

        workflow_abs_path = workflow_persistant.store.path
        workflow_name = workflow_abs_path.split("/")[-1]
        destination = workflow_persistant.attrs["tasks"][task_idx]["basefolder"]
        codedir =  workflow_persistant.attrs["tasks"][task_idx]["codefolder"]
        workflow_remote = Path(destination) / Path(workflow_name)
        location = "remote"
        task = workflow_persistant.attrs["tasks"][task_idx]

        # Force update of zattrs
        file_handler.force_zattrs_update(
            workflow_abs_path, 
            workflow_persistant.attrs.asdict()
        )

        # Copy workflow to remote
        self.remote_clients[task["hostname"]].bulk_upload(destination, [workflow_abs_path])

        # Launch remote instance pointing at workflow

        handover_command = f'python RunWorkflow {workflow_remote} {location}'
        self.remote_clients[task["hostname"]].execute_commands(codedir, handover_command)

        exit()


    def handover_remote_to_local(self):

        pass