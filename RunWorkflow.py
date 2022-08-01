import sys

from hpcflow_execution import front_end

if __name__ == '__main__':

    workflow_name = sys.argv[1]

    workflow_json = front_end.load_workflow_from_json(workflow_name)

    front_end.run_workflow(workflow_json)