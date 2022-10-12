import msal
import os
from pathlib import Path
import requests

from hpcflow_execution.CloudStorage import CloudStorage
import hpcflow_execution.CloudExceptions as CloudExceptions

GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"


class CloudOneDrive(CloudStorage):
    def __init__(self, client_id, scopes):
        super().__init__(client_id)
        self.scopes = scopes

    def authorize(self):
        """ "Get and save authorization and refresh tokens for use at a later
        date."""

        token_cache = self.get_authorization()
        self.save_token_cache(token_cache)

    def upload_files(self, local_path, files, remote_path):
        """ "Use authentication to create access token and upload files."""

        token_cache = self.load_token_cache()
        access_token = self.get_access_token(token_cache)
        for file in files:
            self.upload_file(access_token, local_path, file, remote_path)

    def remove_authorization(self):
        """Delete token cache file."""
        # Add client.remove_account(account) to sign user out and remove from
        # cache?

        self.remove_token_cache()

    def get_authorization(self):
        """Authorize and return token cache."""

        token_cache = msal.SerializableTokenCache()

        client = msal.PublicClientApplication(
            client_id=self.client_id, token_cache=token_cache
        )

        flow = client.initiate_device_flow(scopes=self.scopes)
        print(flow["message"])
        client.acquire_token_by_device_flow(flow)

        return token_cache

    def save_token_cache(self, token_cache):
        """Save provided token cache"""

        token_path = "config/ms_graph_api_token.json"

        with open(token_path, "w") as file:
            file.write(token_cache.serialize())

    def load_token_cache(self):
        """Load token cache from disk and return"""

        token_path = "config/ms_graph_api_token.json"
        token_cache = msal.SerializableTokenCache()

        if os.path.exists(token_path):
            with open(token_path, "r") as file:
                token_cache.deserialize(file.read())
        else:
            raise CloudExceptions.OneDriveAuthError

        return token_cache

    def remove_token_cache(self):
        """Delete token cache file."""
        # Test for file not existing

        token_path = "config/ms_graph_api_token.json"

        try:
            os.remove(token_path)
        except FileNotFoundError:
            print(f"Trying to delete non-existant OneDrive token file {token_path}!")
            raise

    def get_access_token(self, token_cache):

        """Get access token using provided token_cache"""

        client = msal.PublicClientApplication(
            client_id=self.client_id, token_cache=token_cache
        )

        accounts = client.get_accounts()

        if accounts:
            access_token = client.acquire_token_silent(self.scopes, accounts[0])
            # Check if token cache changed (eg because refresh token was used)
            # and save if changed.
            if token_cache.has_state_changed:
                self.save_token_cache(token_cache)
        else:
            raise CloudExceptions.OneDriveAuthError

        return access_token

    def upload_file(self, access_token, local_path, file, remote_path):

        local_path_to_file = Path(local_path) / file
        remote_path_to_file = Path(remote_path) / file

        headers = {"Authorization": "Bearer " + access_token["access_token"]}

        with open(local_path_to_file, "rb") as upload:
            file_content = upload.read()

        requests.put(
            GRAPH_API_ENDPOINT
            + f"/me/drive/items/root:/{remote_path_to_file}:/content",
            headers=headers,
            data=file_content,
        )


#    def generate_access_token(self, user_present=False):
#
#        """Returns access token. Authenticates if needed"""
#
#        # NOTE: very general purpose - don't want this to try and authenticate
#        # while running remotely.
#
#        client_id = self.client_id
#        scopes = self.scopes
#
#        token_path = "config/ms_graph_api_token.json"
#
#        token_cache = msal.SerializableTokenCache()
#
#        # If token file exists, read it in. Check if it has expired. If it has
#        # delete token and create new cache.
#
#        if os.path.exists(token_path):
#
#            with open(token_path, "r") as file:
#
#                token_cache.deserialize(file.read())
#                token_detail = json.load(
#                    open(
#                        token_path,
#                    )
#                )
#                token_detail_key = list(token_detail["AccessToken"].keys())[0]
#                token_expiration = datetime.fromtimestamp(
#                    int(token_detail["AccessToken"][token_detail_key]["expires_on"])
#                )
#
#                if datetime.now() > token_expiration:
#                    os.remove(token_path)
#                    token_cache = msal.SerializableTokenCache()
#
#        client = msal.PublicClientApplication(
#            client_id=client_id, token_cache=token_cache
#        )
#
#        # Check if accounts exist. If not, authenticate. Raise exception if
#        # need to authenticate and user not present.
#        accounts = client.get_accounts()
#        if accounts:
#            print(accounts)
#            access_token = client.acquire_token_silent(scopes, accounts[0])
#        elif user_present:
#            flow = client.initiate_device_flow(scopes=scopes)
#            print(flow["message"])
#            access_token = client.acquire_token_by_device_flow(flow)
#        else:
#            raise CloudExceptions.UserInputError
#
#        with open(token_path, "w") as file:
#            file.write(token_cache.serialize())
#
#        return access_token

#    def test_upload(self):
#
#        file_path = "test.txt"
#
#        access_token = self.generate_access_token()
#
#        headers = {"Authorization": "Bearer " + access_token["access_token"]}
#
#        with open(file_path, "rb") as upload:
#            file_content = upload.read()
#
#        response = requests.put(
#            GRAPH_API_ENDPOINT + f"/me/drive/items/root:/{file_path}:/content",
#            headers=headers,
#            data=file_content,
#        )
#
#        print(response.json())
#
