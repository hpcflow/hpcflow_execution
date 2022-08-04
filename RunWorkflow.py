import sys

from hpcflow_execution import FrontEnd

if __name__ == '__main__':

    workflow_name = sys.argv[1]

    exec_location = sys.argv[2]

    fe = FrontEnd.FrontEnd(exec_location)

    workflow_json = fe.load_workflow_from_json(workflow_name)

    FrontEnd.run_workflow(workflow_json)