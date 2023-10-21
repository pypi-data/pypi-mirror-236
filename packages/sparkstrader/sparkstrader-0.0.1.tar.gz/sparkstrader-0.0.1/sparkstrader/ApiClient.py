"""apiclient.py"""

import sys
from rich.console import Console
from rich.progress import track

from .Api.AuthApi import Auth
from .Api.ExchangeApi import ExchangeApi

# minimal traceback
sys.tracebacklimit = 1


class ApiClient:
    """API Client"""

    Login: bool = False
    """
    Login indicate if logined.
    """

    Exchange: ExchangeApi = None

    def __init__(
        self,
        authTokenUrl: str = "https://www.sparkstrader.com/connect/token",
        apiUrl: str = "https://www.sparkstrader.com/api",
    ) -> None:
        self.authTokenUrl = authTokenUrl
        self.apiUrl = apiUrl
        self.console = Console()

    def Login(self, username: str, password: str) -> bool:
        """
        Login to the API using the specified username and password.

        Args:
            username: The username for authentication.
            password: The password for authentication.

        Returns:
            bool: True if the login is successful, False otherwise.

        Raises:
            None.
        """
        auth = Auth()
        authinfo = {
            "client_id": "Sparks_App",
            "scope": "Sparks",
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        self.AccessToken = auth.GetAccessToken(self.authTokenUrl, authinfo)
        print(f"AccessToken:{self.AccessToken}")
        self.Login = self.AccessToken is not None
        if self.Login:
            self.Exchange = ExchangeApi(self.apiUrl, self.AccessToken)
        return self.Login
