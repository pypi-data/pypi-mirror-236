import sys
import requests
from json.decoder import JSONDecodeError
from requests import ConnectionError as requests_ConnectionError
from requests import Timeout as requests_Timeout
from requests.exceptions import HTTPError as requests_HTTPError
from rich.console import Console


class Auth:
    def __init__(self) -> None:
        self.console = Console()

    def GetAccessToken(self, endpoint: str, auth_info: dict) -> str:
        if not endpoint.strip():
            raise ValueError("endpoint is empty!")

        try:
            # 通过password flow模式，获取access token
            head = {"Content-Type": "application/x-www-form-urlencoded"}
            # auth_info = {
            #    "client_id": "Sparks_App",
            #    "scope": "Sparks",
            #    "grant_type": "password",
            #    "username": "admin",
            #    "password": "1q2w3E*",
            # }
            resp = requests.post(
                endpoint,
                data=auth_info,
                headers=head,
                verify=False,
            )

            if resp.status_code != 200:
                try:
                    if "message" in resp.json():
                        resp_message = resp.json()["message"]
                    elif "errors" in resp.json():
                        self.console.log(resp.json())
                        sys.exit(1)
                    else:
                        resp_message = ""

                    message = f"({resp.status_code}) {self._api_url} - {resp_message}"
                    self.console.log(message)

                except JSONDecodeError as err:
                    self.console.log(err)

            try:
                resp.raise_for_status()

                return resp.json()["access_token"]
            except ValueError as err:
                self.console.log(err)

        except requests_ConnectionError as err:
            self.console.log(err)
        except requests_HTTPError as err:
            self.console.log(err)
        except requests_Timeout as err:
            self.console.log(err)
        return None


# import sys

# sys.path.insert(0, f"{sys.path[0]}/../../")
# from sparks import config as cfg
#
# if __name__ == "__main__":
#    print(cfg.AuthTokenUrl)
#    auth = Auth()
#    accessToken = auth.GetAccessToken(cfg.AuthTokenUrl, cfg.Auth_Info)
#    print(accessToken)
