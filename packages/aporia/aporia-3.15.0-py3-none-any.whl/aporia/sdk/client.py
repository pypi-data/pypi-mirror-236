from typing import Dict, Optional, Tuple

import requests


class Client:
    def __init__(self, base_url: str, token: str, debug: bool = False):
        self.base_url = base_url
        self.token = token
        self.debug = debug

    def send_request(
        self,
        url: str,
        method: str,
        data: Optional[Dict] = None,
        url_override: Optional[str] = None,
        url_search_replace: Optional[Tuple[str, str]] = None,
    ):
        if url_override is not None:
            target_url = url_override
        else:
            target_url = self.base_url + url

        if url_search_replace is not None:
            target_url = target_url.replace(url_search_replace[0], url_search_replace[1])

        if self.debug:
            print(f"{method} {target_url}, ({data})", end=" -> ")

        response = requests.request(
            method=method,
            url=target_url,
            json=data,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        if self.debug:
            print(f"{response.status_code}")

        return response

    def assert_response(self, response: requests.Response):
        if not response.ok:
            try:
                body = response.json()
            except Exception:
                body = response.content
            if self.debug:
                print(f"Request failed with status {response.status_code}, body: {body}")
            raise RuntimeError(f"Request failed with status {response.status_code}, body: {body}")
