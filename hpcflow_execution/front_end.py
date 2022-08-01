import json
import sys

from hpcflow_execution import execution

def run_workflow(workflow_json):

    workflow_dict = json.loads(workflow_json)

    execution.run_elements(workflow_dict)

def load_workflow_from_json(filename):

    with open(filename) as file:
        workflow_json = file.read()

    return workflow_json





