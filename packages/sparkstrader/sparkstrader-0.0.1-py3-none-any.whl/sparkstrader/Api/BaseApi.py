from json.decoder import JSONDecodeError
import sys
import requests
from requests import get as requests_get
from requests import ConnectionError as requests_ConnectionError
from requests import Timeout as requests_Timeout
from requests.exceptions import HTTPError as requests_HTTPError
from rich.console import Console
import sys


class BaseApi:
    def __init__(self, apiUrl: str, accessToken: str) -> None:
        self.console = Console()
        self.accessToken = accessToken
        self.apiUrl = apiUrl

    def _rest_get_method(self, endpoint: str, uri: str = None, params: dict = None):
        """Generic REST GET"""

        if not endpoint.strip():
            raise ValueError("endpoint is empty!")

        try:
            head = {"Authorization": f"Bearer {self.accessToken}"}
            url = f"{self.apiUrl}/{endpoint}"
            # if uri
            if uri is not None:
                url = f"{url}/{uri}"

            resp = requests_get(url, headers=head, params=params, verify=False)
            path = resp.request.path_url

            if resp.status_code != 200:
                try:
                    if "message" in resp.json():
                        resp_message = resp.json()["message"]
                    elif "error" in resp.json():
                        self.console.log(resp.json())
                        sys.exit(1)
                    else:
                        resp_message = ""

                    message = f"({resp.status_code}) {self.apiUrl} - {resp_message}"
                    self.console.log(message)

                except JSONDecodeError as err:
                    self.console.log(err)

            try:
                resp.raise_for_status()

                # return resp.text
                return resp.json()

            except ValueError as err:
                self.console.log(err)

        except requests_ConnectionError as err:
            self.console.log(err)
        except requests_HTTPError as err:
            self.console.log(err)
        except requests_Timeout as err:
            self.console.log(err)
        return {}

    def _rest_post_method(self, endpoint: str, uri: str = None, json: dict = None):
        """Generic REST post"""

        if not endpoint.strip():
            raise ValueError("endpoint is empty!")

        try:
            head = {"Authorization": f"Bearer {self.accessToken}"}
            url = f"{self.apiUrl}/{endpoint}"
            # if uri
            if uri is not None:
                url = f"{url}/{uri}"

            resp = requests.post(url, headers=head, json=json, verify=False)

            if resp.status_code != 200:
                try:
                    if "message" in resp.json():
                        resp_message = resp.json()["message"]
                    elif "error" in resp.json():
                        self.console.log(resp.json())
                        sys.exit(1)
                    else:
                        resp_message = ""

                    message = f"({resp.status_code}) {self.apiUrl} - {resp_message}"
                    self.console.log(message)

                except JSONDecodeError as err:
                    self.console.log(err)

            try:
                resp.raise_for_status()

                # return resp.text
                return resp.json()

            except ValueError as err:
                self.console.log(err)

        except requests_ConnectionError as err:
            self.console.log(err)
        except requests_HTTPError as err:
            self.console.log(err)
        except requests_Timeout as err:
            self.console.log(err)
        return {}

    def _rest_put_method(self, endpoint: str, uri: str = None, json: dict = None):
        """Generic REST put"""

        if not endpoint.strip():
            raise ValueError("endpoint is empty!")

        try:
            head = {"Authorization": f"Bearer {self.accessToken}"}
            url = f"{self.apiUrl}/{endpoint}"
            # if uri
            if uri is not None:
                url = f"{url}/{uri}"

            resp = requests.put(url, headers=head, json=json, verify=False)

            if resp.status_code != 200:
                try:
                    if "message" in resp.json():
                        resp_message = resp.json()["message"]
                    elif "error" in resp.json():
                        self.console.log(resp.json())
                        sys.exit(1)
                    else:
                        resp_message = ""

                    message = f"({resp.status_code}) {self.apiUrl} - {resp_message}"
                    self.console.log(message)

                except JSONDecodeError as err:
                    self.console.log(err)

            try:
                resp.raise_for_status()

                # return resp.text
                return resp.json()

            except ValueError as err:
                self.console.log(err)

        except requests_ConnectionError as err:
            self.console.log(err)
        except requests_HTTPError as err:
            self.console.log(err)
        except requests_Timeout as err:
            self.console.log(err)
        return {}

    def _rest_delete_method(self, endpoint: str, uri: str = None):
        """Generic REST delete"""

        if not endpoint.strip():
            raise ValueError("endpoint is empty!")

        try:
            head = {"Authorization": f"Bearer {self.accessToken}"}
            url = f"{self.apiUrl}/{endpoint}"
            # if uri
            if uri is not None:
                url = f"{url}/{uri}"

            resp = requests.delete(url, headers=head, verify=False)

            # 204 代表成功
            if resp.status_code != 204:
                try:
                    if "message" in resp.json():
                        resp_message = resp.json()["message"]
                    elif "error" in resp.json():
                        self.console.log(resp.json())
                        sys.exit(1)
                    else:
                        resp_message = ""

                    message = f"({resp.status_code}) {self.apiUrl} - {resp_message}"
                    self.console.log(message)

                except JSONDecodeError as err:
                    self.console.log(err)

            try:
                resp.raise_for_status()

                # return resp.text
                return True

            except ValueError as err:
                self.console.log(err)

        except requests_ConnectionError as err:
            self.console.log(err)
        except requests_HTTPError as err:
            self.console.log(err)
        except requests_Timeout as err:
            self.console.log(err)
        return False
