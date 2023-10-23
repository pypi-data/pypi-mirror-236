from typing import Any, Dict, List, Optional, Tuple, Union

from aporia.as_code.resources.base import BaseResource, CompareStatus
from aporia.sdk.client import Client
from aporia.sdk.segments import Segment as _Segment


class Segment(BaseResource):
    def __init__(
        self,
        resource_name: str,
        /,
        *,
        name: Optional[str] = None,
        field: Optional[str] = None,
        values: Optional[Union[List[str], List[Union[float, int]]]] = None,
        terms: Optional[List[Tuple[str, str]]] = None,
    ):
        self.name = resource_name
        self.dependants = []
        if name is None:
            name = resource_name

        self._args = {"name": name}
        if field is not None:
            if values is None:
                raise Exception("Must supply values for automatic segment")
            self._args["field_name"] = field
            self._args["values"] = values
        elif terms is not None:
            if values is not None:
                raise Exception("For custom segments, only specify the terms parameter")
            self._args["terms"] = terms
        else:
            raise Exception("Supply either field+values or terms")

    def compare(self, resource_data: Dict) -> CompareStatus:
        values = self._args.get("values", [])
        resource_field_name = resource_data.get("field_name")
        # Old stacks might have the field data stored in an outdated format (due to API change)
        if resource_field_name is None:
            resource_field_data = resource_data.get("field", {})
            resource_field_name = (resource_field_data or {}).get("name")

        if "terms" in self._args.keys():
            values = [term[1] for term in self._args["terms"]]
        if all(
            [
                self._args.get("terms") == resource_data["terms_values"],
                self._args.get("field_name") == resource_field_name,
                values == resource_data["values"],
                self._args["name"] == resource_data["name"],
            ]
        ):
            return CompareStatus.SAME
        elif any(
            [
                self._args.get("terms") != resource_data["terms_values"],
                self._args.get("field_name") != resource_field_name,
                values != resource_data["values"],
            ]
        ):
            return CompareStatus.MISMATCHED
        else:
            return CompareStatus.UPDATEABLE

    def setarg(self, arg_name: str, arg_value: Any):
        self._args[arg_name] = arg_value

    def create(self, client: Client) -> Tuple[str, Dict]:
        segment = _Segment.create(client=client, **self._args)
        return segment.id, segment.raw_data

    def read(self, client: Client, id: str) -> Dict:
        return _Segment.read(client=client, id=id).raw_data

    def update(self, client: Client, id: str) -> Dict:
        segment = _Segment.read(client=client, id=id)
        segment.update(**self._args)
        return segment.raw_data

    @classmethod
    def delete(cls, client: Client, id: str):
        _Segment.delete_by_id(client=client, id=id)

    def get_diff(self, resource_data: Dict) -> Dict:
        diffs = {}
        if self._args["name"] != resource_data["name"]:
            diffs["name"] = (resource_data["name"], self._args["name"])
        return diffs