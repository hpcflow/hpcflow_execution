import collections
import subprocess
import secrets
from pathlib import Path

from hpcflow_execution import file_handler
from hpcflow_execution import RemoteClient


class Execution:
    def __init__(self, machines, current_machine):
        self.machines = machines
        self.current_machine = current_machine
        self.connections = collections.defaultdict(None)
        self.remote_prep_done = set()

    def prep_workflow(self, workflow_dict):

        workflow_id = f'{workflow_dict["name"]}_{secrets.token_hex(10)}'

        scratch_path = self.machines[self.current_machine]["scratch_dir"]

        workflow_persistant = file_handler.create_persistant_workflow(
            workflow_id, workflow_dict, scratch_path
        )

        return workflow_persistant

    def prep_tasks(self, workflow_persistant):

        print("Writing scripts and job submission files.")

        for task_idx, task in enumerate(workflow_persistant.attrs["tasks"]):

            if workflow_persistant.attrs["tasks"][task_idx]["status"] == 0:

                workflow_persistant = file_handler.write_execution_files(
                    task, task_idx, workflow_persistant, self.machines
                )

                workflow_persistant.attrs["tasks"][task_idx]["status"] = 1

        return workflow_persistant

    def prep_connections(self, workflow_persistant, machines, location):

        connections_required = self.build_connection_list(workflow_persistant, location)

        self.connections = self.init_connections_from_current(
            machines, connections_required, location
        )

    def run_tasks(self, workflow_persistant, location):

        for task_idx, task in enumerate(workflow_persistant.attrs["tasks"]):

            current_status = workflow_persistant.attrs["tasks"][task_idx]["status"]

            if task["location"] == location and current_status == 1:

                command_info = subprocess.run(
                    task["execute"], shell=True, cwd=task["exec_dir"]
                )
                command_info.check_returncode()

                status_update = 2

            elif task["location"] != location and current_status == 1:

                self.handover_machine_to_machine(
                    workflow_persistant, location, task["location"]
                )

            else:

                raise Exception("Lost while running tasks!")

            workflow_persistant.attrs["tasks"][task_idx]["status"] = status_update

        return workflow_persistant

    def handover_local_to_remote(self, task_idx, workflow_persistant):

        print("Handing over to remote...")

        workflow_abs_path = workflow_persistant.store.path
        workflow_name = workflow_abs_path.split("/")[-1]
        destination = workflow_persistant.attrs["tasks"][task_idx]["basefolder"]
        codedir = workflow_persistant.attrs["tasks"][task_idx]["codefolder"]
        workflow_remote = Path(destination) / Path(workflow_name)
        location = "remote"
        task = workflow_persistant.attrs["tasks"][task_idx]

        # Force update of zattrs
        file_handler.force_zattrs_update(
            workflow_abs_path, workflow_persistant.attrs.asdict()
        )

        # Copy workflow to remote
        self.remote_clients[task["hostname"]].bulk_upload(
            destination, [workflow_abs_path]
        )

        # Launch remote instance pointing at workflow
        load_conda = "module load apps/anaconda3/5.2.0"
        load_proxy = "module load tools/env/proxy"
        handover_command = f"cd {codedir} && conda run -n test_env python RunWorkflow.py {workflow_remote} {location}"

        # NOTE: must execute all commands in one go - load conda and proxy,
        # cd to code directory and execute python in conda environment.
        # This stuff doesn't get remembered between usages of the open
        # SSH pipe.

        self.remote_clients[task["hostname"]].execute_commands(
            codedir, [f"{load_conda} && {load_proxy} && {handover_command}"]
        )

        exit()

    def handover_machine_to_machine(
        self, workflow_persistant, source_machine, dest_machine
    ):

        print(f"Handover from {source_machine} to {dest_machine}")

        source_workflow_path = workflow_persistant.store.path
        workflow_name = source_workflow_path.split("/")[-1]
        destination = self.machines[dest_machine]["scratch_dir"]
        code_dir = self.machines[dest_machine]["code_dir"]
        workflow_dest = Path(destination) / Path(workflow_name)

        # Force update of zattrs
        file_handler.force_zattrs_update(
            source_workflow_path, workflow_persistant.attrs.asdict()
        )

        connection_type = self.machines[source_machine]["connections"][dest_machine][
            "type"
        ]

        print(connection_type)

        # Copy workflow to remote
        if connection_type == "SSH":
            self.connections[source_machine][dest_machine].bulk_upload(
                destination, [source_workflow_path]
            )

        # Launch remote instance pointing at workflow
        load_conda = "module load apps/anaconda3/5.2.0"
        load_proxy = "module load tools/env/proxy"
        handover_command = f"cd {code_dir} && conda run -n test_env python RunWorkflow.py {workflow_dest} {dest_machine}"

        # NOTE: must execute all commands in one go - load conda and proxy,
        # cd to code directory and execute python in conda environment.
        # This stuff doesn't get remembered between usages of the open
        # SSH pipe.

        self.connections[source_machine][dest_machine].execute_commands(
            code_dir, [f"{load_conda} && {load_proxy} && {handover_command}"]
        )

        exit()

    def handover_remote_to_local(self):

        pass

    def build_connection_list(self, workflow_persistant, current_loc):

        connections_required = collections.defaultdict(dict)

        source_loc = current_loc

        for task in workflow_persistant.attrs["tasks"]:

            dest_loc = task["location"]

            if source_loc != dest_loc:

                connections_required[source_loc][dest_loc] = None

                source_loc = dest_loc

        return connections_required

    def init_connections_from_current(
        self, machines, connections_required, current_loc
    ):

        for dest_loc in connections_required[current_loc].items():

            connection_info = machines[current_loc]["connections"][dest_loc[0]]

            if connection_info["type"] == "SSH":
                connections_required[current_loc][
                    dest_loc[0]
                ] = RemoteClient.RemoteClient(
                    connection_info["hostname"],
                    connection_info["username"],
                    machines[dest_loc[0]]["scratch_dir"],
                )
            elif connection_info["type"] == "OneDrive":
                pass
            else:
                con_type = connection_info["type"]
                raise Exception(f"Unknown connection type {con_type}")

        return connections_required
