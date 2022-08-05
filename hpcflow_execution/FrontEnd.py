import zarr

from hpcflow_execution import Execution

class FrontEnd:

    def __init__(
        self,
        location: str
    ):
        self.location = location

    def __repr__(self):
        return(f"FrontEnd({self.location})")

    def run_workflow(self, workflow):

        executor = Execution.Execution()

        if isinstance(workflow, str):
            workflow_persistant = executor.prep_workflow(workflow)
        elif isinstance(workflow, zarr.hierarchy.Group):
            workflow_persistant = workflow
        else:
            raise Exception('Workflow type not recognised.')

        workflow_persistant = executor.prep_tasks(workflow_persistant)

        workflow_persistant = executor.run_tasks(workflow_persistant, self.location)

    def load_from_json(self, filename):

        with open(filename) as file:
            workflow_json = file.read()

        return workflow_json

    def load_from_persistant_workflow(self, filename):

        with zarr.open(filename, 'r+') as file:
            workflow_persistant = file

        return workflow_persistant





