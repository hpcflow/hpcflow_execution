import msal
import os
import json
from datetime import datetime
import requests

from hpcflow_execution import CloudStorage

GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"


class CloudOneDrive(CloudStorage):
    def __init__(self, client_id, scopes):
        super().__init__(client_id)
        self.scopes = scopes

    def generate_access_token(self):

        client_id = self.client_id
        scopes = self.scopes

        token_path = "ms_graph_api_token.json"

        token_cache = msal.SerializableTokenCache()

        if os.path.exists(token_path):

            with open(token_path, "r") as file:

                token_cache.deserialize(file.read())
                token_detail = json.load(
                    open(
                        token_path,
                    )
                )
                token_detail_key = list(token_detail["AccessToken"].keys())[0]
                token_expiration = datetime.fromtimestamp(
                    int(token_detail["AccessToken"][token_detail_key]["expires_on"])
                )

                if datetime.now() > token_expiration:
                    os.remove(token_path)
                    token_cache = msal.SerializableTokenCache()

        client = msal.PublicClientApplication(
            client_id=client_id, token_cache=token_cache
        )

        accounts = client.get_accounts()
        if accounts:
            print(accounts)
            token_response = client.acquire_token_silent(scopes, accounts[0])
        else:
            flow = client.initiate_device_flow(scopes=scopes)
            print(flow["message"])
            token_response = client.acquire_token_by_device_flow(flow)

        with open(token_path, "w") as file:
            file.write(token_cache.serialize())

        return token_response

    def test_upload(self):

        file_path = "test.txt"

        access_token = self.generate_access_token()

        headers = {"Authorization": "Bearer " + access_token["access_token"]}

        with open(file_path, "rb") as upload:
            file_content = upload.read()

        response = requests.put(
            GRAPH_API_ENDPOINT + f"/me/drive/items/root:/{file_path}:/content",
            headers=headers,
            data=file_content,
        )

        print(response.json())
