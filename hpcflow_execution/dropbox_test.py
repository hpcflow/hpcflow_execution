from textwrap import dedent
from pathlib import Path

import dropbox as dropbox_api


DBX_APP_KEY = "638ebfutlda13wu"


def get_token():

    APP_KEY = DBX_APP_KEY
    auth_flow = dropbox_api.DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True)
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

    return token


def get_dropbox(token):

    dbx = dropbox_api.Dropbox(token)

    return dbx


def upload_file(dbx, local_path, local_file, dropbox_path):

    local_file_path = Path(local_path) / local_file

    mode = dropbox_api.files.WriteMode("overwrite")

    with local_file_path.open(mode="rb") as file_handle:
        dbx.files_upload(file_handle.read(), dropbox_path, mode=mode)
