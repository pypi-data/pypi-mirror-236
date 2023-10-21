"""constant"""


import sys

AccessToken = None

IsDebug = bool(sys.gettrace())
if IsDebug:
    AuthTokenUrl = "https://localhost:44319/connect/token"
    Auth_Info = {
        "client_id": "Sparks_App",
        "scope": "Sparks",
        "grant_type": "password",
        "username": "admin",
        "password": "1q2w3E*",
    }

    ApiUrl = "https://localhost:44319/api"

else:
    AuthTokenUrl = "https://wwww.sparkstrader.com/connect/token"
    Auth_Info = {
        "client_id": "Sparks_App",
        "scope": "Sparks",
        "grant_type": "password",
        "username": "admin",
        "password": "1q2w3E*",
    }

    ApiUrl = "https://wwww.sparkstrader.com/api"
