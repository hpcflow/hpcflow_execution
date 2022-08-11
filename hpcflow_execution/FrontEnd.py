import json

import zarr

from hpcflow_execution import Execution


class FrontEnd:
    def __init__(self, location: str):
        self.location = location

    def __repr__(self):
        return f"FrontEnd({self.location})"

    def run_workflow(self, workflow):

        executor = Execution.Execution()

        if isinstance(workflow, dict):
            workflow_persistant = executor.prep_workflow(workflow)
        elif isinstance(workflow, zarr.hierarchy.Group):
            workflow_persistant = workflow
        else:
            raise Exception("Workflow type not recognised.")

        workflow_persistant = executor.prep_tasks(workflow_persistant)

        workflow_persistant = executor.run_tasks(workflow_persistant, self.location)

    def load_from_json_to_dict(self, filename):

        with open(filename) as file:
            json_string = file.read()

        json_in_dict = json.loads(json_string)

        return json_in_dict

    def load_from_persistant_workflow(self, filename):

        with zarr.open(filename, "r+") as file:
            workflow_persistant = file

        return workflow_persistant
