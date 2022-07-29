import json
import sys

if __name__ == '__main__':

    workflow_name = sys.argv[1]

    with open(workflow_name) as file:
        workflow_string = file.read()

    workflow_dict = json.loads(workflow_string)

    print(workflow_dict)