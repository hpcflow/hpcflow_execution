# test_CloudOneDrive.py

import pytest

from hpcflow_execution.CloudOneDrive import CloudOneDrive
import hpcflow_execution.CloudExceptions as CloudExceptions


def test_load_token_cache_file_does_not_exist():
    """load_token_cache raises OneDriveAuthError if token file does not
    exist"""

    od_app_key = "123456789"
    od_app_scopes = ["scope_1", "scope_2"]

    CloudOD = CloudOneDrive(od_app_key, od_app_scopes)

    with pytest.raises(CloudExceptions.OneDriveAuthError):
        CloudOD.load_token_cache()


def test_remove_token_cache_file_does_not_exist():
    """remove_token_cache raises FileNotFoundError if token file does not
    exist"""

    od_app_key = "123456789"
    od_app_scopes = ["scope_1", "scope_2"]

    CloudOD = CloudOneDrive(od_app_key, od_app_scopes)

    with pytest.raises(FileNotFoundError):
        CloudOD.remove_token_cache()


def test_file_upload_local_path_does_not_exist():
    """file_upload raises FileNotFoundError if specified file path does not
    exist."""

    od_app_key = "123456789"
    od_app_scopes = ["scope_1", "scope_2"]

    CloudOD = CloudOneDrive(od_app_key, od_app_scopes)

    # make these relative
    local_path = "NOT_A_PATH"
    file = "test_upload_file.txt"
    od_path = ""
    od_access_token = {"access_token": "123456"}

    with pytest.raises(FileNotFoundError):
        CloudOD.upload_file(od_access_token, local_path, file, od_path)


def test_file_upload_local_file_does_not_exist():
    """file_upload raises FileNotFoundError if specified local file does not
    exist."""

    od_app_key = "123456789"
    od_app_scopes = ["scope_1", "scope_2"]

    CloudOD = CloudOneDrive(od_app_key, od_app_scopes)

    # make these relative
    local_path = "/Users/user/Documents/projects/hpcflow_execution/tests/test_data"
    file = "NOT_A_FILE"
    od_path = ""
    od_access_token = {"access_token": "123456"}

    with pytest.raises(FileNotFoundError):
        CloudOD.upload_file(od_access_token, local_path, file, od_path)
