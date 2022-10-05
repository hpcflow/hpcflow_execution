import json

from textwrap import dedent
from pathlib import Path
from datetime import datetime
import os
import sys
import dropbox as dropbox_api

from hpcflow_execution.CloudStorage import CloudStorage
from hpcflow_execution.JSONEncoders import DateTimeAwareEncoder


class CloudDropbox(CloudStorage):
    def __init__(self, client_id, scopes):
        super().__init__(client_id)
        self.scopes = scopes

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

        token_string = json.dumps(auth_dict, cls=DateTimeAwareEncoder)

        with open(token_path, "w") as file_out:
            json.dump(token_string, file_out, indent=4)

    def load_authorizaton(self):

        token_path = "config/dropbox_api_token.json"

        try:
            with open(token_path, "r") as file_in:
                auth_string = file_in.read()
        except FileNotFoundError:
            print(f"File {token_path} not found!", file=sys.stderr)
            return
        except PermissionError:
            print(f"Insufficient permission to read {token_path}!", file=sys.stderr)
            return
        except IsADirectoryError:
            print(f"{token_path} is a directory!", file=sys.stderr)
            return

        auth_dict = json.loads(auth_string)

        return auth_dict

    def delete_authorization_file(self):

        token_path = "config/dropbox_api_token.json"

        os.remove(token_path)

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

        local_file_path = Path("/" + local_path) / local_file

        mode = dropbox_api.files.WriteMode("overwrite")

        with local_file_path.open(mode="rb") as file_handle:
            dbx.files_upload(file_handle.read(), dropbox_path, mode=mode)
