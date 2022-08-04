from hpcflow_execution import Execution

class FrontEnd:

    def __init__(
        self,
        location: str
    ):
        self.location = location

    def __repr__(self):
        return(f"FrontEnd({self.location})")

    def run_workflow(self, workflow_json):

        executor = Execution.Execution()

        workflow_persistant = executor.prep_workflow(workflow_json)

        workflow_persistant = executor.prep_tasks(workflow_persistant)

        workflow_persistant = executor.run_tasks(workflow_persistant, self.location)

    def load_workflow_from_json(self, filename):

        with open(filename) as file:
            workflow_json = file.read()

        return workflow_json





