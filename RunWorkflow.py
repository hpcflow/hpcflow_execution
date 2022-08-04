import sys

from hpcflow_execution import FrontEnd

if __name__ == '__main__':

    workflow_name = sys.argv[1]

    workflow_json = FrontEnd.load_workflow_from_json(workflow_name)

    FrontEnd.run_workflow(workflow_json)