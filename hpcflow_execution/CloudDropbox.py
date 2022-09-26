import json

from textwrap import dedent
from pathlib import Path
import dropbox as dropbox_api

from hpcflow_execution.CloudStorage import CloudStorage


class CloudDropbox(CloudStorage):
    def __init__(self, client_id, scopes):
        super().__init__(client_id)
        self.scopes = scopes

    def generate_access_token(self):

        APP_KEY = self.client_id
        auth_flow = dropbox_api.DropboxOAuth2FlowNoRedirect(
            APP_KEY, use_pkce=True, scope=self.scopes
        )
        authorize_url = auth_flow.start()

        msg = dedent(
            f"""
        --------------------------- Connecting hpcflow to Dropbox ----------------------------
            1. Go to this URL:
            {authorize_url}
            2. Click "Allow" (you might have to log in first).
            3. Copy the authorization code below.
        --------------------------------------------------------------------------------------
        """
        )
        print(msg)

        auth_code = input("Enter the authorization code here: ").strip()
        oauth_result = auth_flow.finish(auth_code)
        token = oauth_result.access_token

        token_dict = {"AccessToken": token}

        return token_dict

    def save_token(self, token_dict):

        token_path = "config/dropbox_api_token.json"

        token_string = json.dumps(token_dict)

        with open(token_path, "w") as file_out:
            file_out.write(token_string)

    def get_dropbox(self, token_dict):

        token = token_dict["AccessToken"]

        dbx = dropbox_api.Dropbox(token)

        return dbx

    def upload_file(self, dbx, local_path, local_file, dropbox_path):

        local_file_path = Path(local_path) / local_file

        mode = dropbox_api.files.WriteMode("overwrite")

        with local_file_path.open(mode="rb") as file_handle:
            dbx.files_upload(file_handle.read(), dropbox_path, mode=mode)
