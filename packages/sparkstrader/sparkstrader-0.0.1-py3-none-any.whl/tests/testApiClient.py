import sys

# from ..sparks.ApiClient import ApiClient

sys.path.insert(0, f"{sys.path[0]}/..")
from sparkstrader.ApiClient import ApiClient

AuthTokenUrl = "https://localhost:44319/connect/token"
ApiUrl = "https://localhost:44319/api"

api = ApiClient(AuthTokenUrl, ApiUrl)
login = api.Login("admin", "1q2w3E*")
print(f"Login:{login}")
