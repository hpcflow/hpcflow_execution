import json

from textwrap import dedent
from pathlib import Path
from datetime import datetime
import os
import sys
import dropbox as dropbox_api

from hpcflow_execution.CloudStorage import CloudStorage
from hpcflow_execution.JSONCoders import DateTimeAwareDecoder, DateTimeAwareEncoder


class CloudDropbox(CloudStorage):
    def __init__(self, client_id, scopes):
        super().__init__(client_id)
        self.scopes = scopes

    def authorize(self):
        """ "Get and save authorization and refresh tokens for use at a later
        date."""

        auth_dict = self.get_authorization()
        self.save_authorization(auth_dict)

    def upload_files(self, local_path, local_files, dropbox_path):
        """ "Use authentication to create dropbox client and upload files."""

        auth_dict = self.load_authorizaton()
        dbx_client = self.get_dropbox_with_refresh(auth_dict)
        for file in local_files:
            self.upload_files(dbx_client, local_path, file, dropbox_path)

        return dbx_client

    def remove_autorization(self, dbx_client):
        """ "Revoke authorization and delete file containing tokens."""

        self.revoke_auth(dbx_client)
        self.delete_authorization_file()

    def get_authorization(self):

        auth_flow = dropbox_api.DropboxOAuth2FlowNoRedirect(
            self.client_id,
            use_pkce=True,
            scope=self.scopes,
            token_access_type="offline",
        )

        authorization_url = auth_flow.start()

        msg = dedent(
            f"""
        --------------------------- Connecting hpcflow to Dropbox ----------------------------
            1. Go to this URL:
            {authorization_url}
            2. Click "Allow" (you might have to log in first).
            3. Copy the authorization code below.
        --------------------------------------------------------------------------------------
        """
        )
        print(msg)

        auth_code = input("Enter the authorization code here: ").strip()
        oauth_result = auth_flow.finish(auth_code)

        return oauth_result.__dict__

    def save_authorization(self, auth_dict):

        token_path = "config/dropbox_api_token.json"

        # token_string = json.dumps(auth_dict, cls=DateTimeAwareEncoder)

        with open(token_path, "w") as file_out:
            json.dump(auth_dict, file_out, indent=4, cls=DateTimeAwareEncoder)

    def load_authorizaton(self):

        # Test for file not exisiting

        token_path = "config/dropbox_api_token.json"

        try:
            with open(token_path, "r") as file_in:
                auth_string = file_in.read()
            auth_dict = json.loads(auth_string, cls=DateTimeAwareDecoder)
            return auth_dict
        except FileNotFoundError:
            print(
                f"Dropbox authorisation file {token_path} not found!", file=sys.stderr
            )
            raise
        except PermissionError:
            print(
                f"Insufficient permission to read Dropbox authorisation file {token_path}!",
                file=sys.stderr,
            )
            raise
        except IsADirectoryError:
            print(f"{token_path} is a directory!", file=sys.stderr)
            raise

    def delete_authorization_file(self):

        # Test for file not existing

        token_path = "config/dropbox_api_token.json"

        try:
            os.remove(token_path)
        except FileNotFoundError:
            print(f"Trying to delete non-existant Dropbox auth file {token_path}!")
            raise

    def check_access_token_expiry(self, auth_dict):

        token_expiry_time = auth_dict["expires_at"]

        if datetime.now() > token_expiry_time:
            return False
        else:
            return True

    def get_dropbox_with_refresh(self, auth_dict):

        token = auth_dict["access_token"]
        token_expiry = auth_dict["expires_at"]
        refresh_token = auth_dict["refresh_token"]

        dbx = dropbox_api.Dropbox(
            oauth2_access_token=token,
            oauth2_refresh_token=refresh_token,
            oauth2_access_token_expiration=token_expiry,
            app_key=self.client_id,
        )

        return dbx

    def revoke_auth(self, dbx):

        dbx.auth_token_revoke()

    def upload_file(self, dbx, local_path, local_file, dropbox_path):

        local_path_to_file = Path(local_path) / local_file

        mode = dropbox_api.files.WriteMode("overwrite")

        try:
            with local_path_to_file.open(mode="rb") as file_handle:
                dbx.files_upload(file_handle.read(), dropbox_path, mode=mode)
        except FileNotFoundError:
            if ~Path(local_path).is_dir():
                print("Path does not exist!")
                raise
            elif ~local_path_to_file.is_file():
                print("File does not exist!")
                raise
