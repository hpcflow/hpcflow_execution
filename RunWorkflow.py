import sys

from hpcflow_execution import FrontEnd

if __name__ == "__main__":

    workflow_name = sys.argv[1]

    exec_location = sys.argv[2]

    machines_config_file = "config/machines.json"

    fe = FrontEnd.FrontEnd(exec_location)

    if ".json" in workflow_name:
        workflow = fe.load_from_json_to_dict(workflow_name)
    elif ".zarr" in workflow_name:
        workflow = fe.load_from_persistant_workflow(workflow_name)
    else:
        raise Exception("Workflow file type not recognised - must be json or zarr")

    machines_dict = fe.load_from_json_to_dict(machines_config_file)

    fe.run_workflow(workflow)
