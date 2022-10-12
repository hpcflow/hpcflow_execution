import json

from hpcflow_execution.CloudOneDrive import CloudOneDrive

config_filename = "config/cloud_config.json"

with open(config_filename, "r") as file_in:
    config_string = file_in.read()
    config_dict = json.loads(config_string)

CloudOD = CloudOneDrive(
    config_dict["azure"]["client_id"], config_dict["azure"]["scopes"]
)

CloudOD.authorize()

local_path = "/Users/user/Documents/projects/hpcflow_execution"
file = "test.txt"
remote_path = ""

CloudOD.upload_files(local_path, [file], remote_path)
