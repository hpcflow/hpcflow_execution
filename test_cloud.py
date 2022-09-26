import json

from hpcflow_execution.CloudDropbox import CloudDropbox
from hpcflow_execution.CloudOneDrive import CloudOneDrive

if __name__ == "__main__":

    config_filename = "config/cloud_config.json"

    with open(config_filename) as file:
        json_string = file.read()

    config = json.loads(json_string)

    # Test CloudDropbox

    dbx_client_id = config["dropbox"]["client_id"]
    dbx_scopes = config["dropbox"]["scopes"]

    test_dbx = CloudDropbox(dbx_client_id, dbx_scopes)
    token_dict = test_dbx.generate_access_token()
    test_dbx.save_token(token_dict)
    test_dbx_client = test_dbx.get_dropbox(token_dict)

    test_dbx.upload_file(
        test_dbx_client,
        "/Users/user/Documents/projects/hpcflow_execution",
        "test.txt",
        "/Apps/hpcflow_execution_test/",
    )

    # Test CloudOneDrive

    OD_client_id = config["azure"]["client_id"]
    OD_scopes = config["azure"]["scopes"]

    test_OD = CloudOneDrive(OD_client_id, OD_scopes)
    test_OD.generate_access_token()
    test_OD.test_upload()

    exit()
