# test_CloudDropbox.py

import pytest
from unittest.mock import Mock

from hpcflow_execution.CloudDropbox import CloudDropbox


def test_load_authorization_auth_file_does_not_exist():

    dbx_app_key = "123456789"
    dbx_app_scopes = ["scope_1", "scope_2"]

    CloudDbx = CloudDropbox(dbx_app_key, dbx_app_scopes)

    with pytest.raises(FileNotFoundError):
        CloudDbx.load_authorizaton()


def test_delete_authorization_file_auth_file_does_not_exist():

    dbx_app_key = "123456789"
    dbx_app_scopes = ["scope_1", "scope_2"]

    CloudDbx = CloudDropbox(dbx_app_key, dbx_app_scopes)

    with pytest.raises(FileNotFoundError):
        CloudDbx.delete_authorizaton_file()


def test_file_upload_local_path_does_not_exist():

    dbx_app_key = "123456789"
    dbx_app_scopes = ["scope_1", "scope_2"]

    CloudDbx = CloudDropbox(dbx_app_key, dbx_app_scopes)

    # make these relative
    local_path = "NOT_A_PATH"
    file = "test_upload_file.txt"
    dbx_path = "/Apps/hpcflow_execution_test"

    dbx_client = Mock()

    with pytest.raises(FileNotFoundError):
        CloudDbx.upload_file(dbx_client, local_path, file, dbx_path)


def test_file_upload_local_file_does_not_exist():

    dbx_app_key = "123456789"
    dbx_app_scopes = ["scope_1", "scope_2"]

    CloudDbx = CloudDropbox(dbx_app_key, dbx_app_scopes)

    # make these relative
    local_path = "/Users/user/Documents/projects/hpcflow_execution/tests/test_data"
    file = "NOT_A_FILE"
    dbx_path = "/Apps/hpcflow_execution_test"

    dbx_client = Mock()

    with pytest.raises(FileNotFoundError):
        CloudDbx.upload_file(dbx_client, local_path, file, dbx_path)
