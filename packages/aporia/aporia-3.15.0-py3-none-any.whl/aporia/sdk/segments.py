from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client


class Segment(BaseAporiaResource):
    def __init__(self, client: Client, data: Dict):
        self.client = client
        self.__update_members(data)

    def __update_members(self, data: Dict):
        self.raw_data = data
        self.id = data["id"]
        self.name = data["name"]
        self.field_name = data["field_name"]
        self.values = data["values"]
        self.terms = data["terms_values"]

    @classmethod
    def get_all(
        cls, client: Client, model_id: Optional[str] = None, manual_only: bool = True
    ) -> List["Segment"]:
        url_params = {}
        if manual_only:
            url_params["is_manually_created"] = "true"
        if model_id is not None:
            url_params["model_id"] = model_id
        encoded_url_params = urlencode(url_params)
        response = client.send_request(
            f"/data-segments{f'?{encoded_url_params}' if len(url_params) > 0 else f''}",
            "GET",
        )

        client.assert_response(response)

        return [cls(client=client, data=entry) for entry in response.json()]

    @classmethod
    def create(
        cls,
        client: Client,
        name: str,
        model_id: str,
        field_name: Optional[str] = None,
        values: Optional[Union[List[str], List[Union[float, int]]]] = None,
        terms: Optional[List[Tuple[str, str]]] = None,
    ) -> "Segment":
        segment_data = {}
        if terms is not None:
            segment_data["terms_values"] = terms
        else:
            segment_data["field_name"] = field_name
            segment_data["values"] = values
        response = client.send_request(
            "/data-segments",
            "POST",
            {"name": name, "model_id": model_id, **segment_data},
        )

        client.assert_response(response)

        return cls(client=client, data=response.json())

    @classmethod
    def read(cls, client: Client, id: str) -> "Segment":
        response = client.send_request(f"/data-segments/{id}", "GET")
        client.assert_response(response)
        return cls(client=client, data=response.json())

    def update(
        self,
        name: Optional[str] = None,
        # field_name: Optional[str] = None,
        values: Optional[Union[List[str], List[Union[float, int]]]] = None,
        terms: Optional[List[Tuple[str, str]]] = None,
        **kwargs,
    ):
        args = {}
        if name is not None:
            args["name"] = name
        # if field_name is not None:
        #     args["field_name"] = field_name
        if values is not None:
            args["values"] = values
        if terms is not None:
            args["terms_values"] = terms
        response = self.client.send_request(
            f"/data-segments/{self.id}",
            "PUT",
            args,
        )
        # response = self.client.send_request(f"/data-segments/{self.id}", "PUT", args)
        self.client.assert_response(response)
        self.__update_members(response.json())

    def delete(self):
        response = self.client.send_request(f"/data-segments/{self.id}", "DELETE")
        self.client.assert_response(response)

    @staticmethod
    def delete_by_id(client: Client, id: str):
        response = client.send_request(f"/data-segments/{id}", "DELETE")
        client.assert_response(response)
