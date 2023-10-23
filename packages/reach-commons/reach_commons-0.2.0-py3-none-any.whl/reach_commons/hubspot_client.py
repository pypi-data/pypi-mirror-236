import json

import requests
from requests.structures import CaseInsensitiveDict


class HubSpotClient:
    def __init__(self, access_token, base_url="https://api.hubapi.com/crm/v3/"):
        self.base_url = base_url
        self.headers = CaseInsensitiveDict(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "authorization": f"Bearer {access_token}",
            }
        )

    def get_business(self, object_type_id, business_id):
        resp = requests.get(
            f"{self.base_url}objects/{object_type_id}/{business_id}",
            headers=self.headers
        )
        return resp

    def update_business(self, business_id, object_type_id, properties):
        resp = requests.patch(
            f"{self.base_url}objects/{object_type_id}/{business_id}?properties=isactive&idProperty=businessid",
            headers=self.headers,
            data=json.dumps({"properties": {**properties}}),
        )
        return resp

    def create_business(self, object_type_id, properties):
        resp = requests.post(
            f"{self.base_url}objects/{object_type_id}?properties=isactive&idProperty=businessid",
            headers=self.headers,
            data=json.dumps({"properties": {**properties}}),
        )
        return resp

    def create_or_update_business(self, object_type_id, business_id, properties):
        resp = self.get_business(object_type_id, business_id)

        if resp.status_code == 200:
            return self.update_business(business_id, object_type_id, properties)

        elif resp.status_code == 404:
            return self.create_business(object_type_id, properties)

        else:
            return resp
