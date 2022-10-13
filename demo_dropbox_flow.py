import json

from hpcflow_execution.CloudDropbox import CloudDropbox

# Read in config details (app key, scopes)

config_filename = "config/cloud_config.json"

with open(config_filename, "r") as file_in:
    config_string = file_in.read()
    config_dict = json.loads(config_string)

# Create dropbox interface object

CloudDbx = CloudDropbox(
    config_dict["dropbox"]["client_id"], config_dict["dropbox"]["scopes"]
)

# Get and save authorization keys

auth_dict = CloudDbx.get_authorization()
print(auth_dict)
CloudDbx.save_authorization(auth_dict)
auth_dict = CloudDbx.load_authorizaton()

print(auth_dict)

# Create client and upload files

dbx_client = CloudDbx.get_dropbox_with_refresh(auth_dict)
CloudDbx.upload_file(
    dbx_client, "/Users/user/Documents/projects/hpcflow_execution", "test.txt", "/"
)

# Revoke access tokens, delete file

CloudDbx.revoke_auth(dbx_client)
# CloudDbx.delete_authorization_file()
