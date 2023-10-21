import pandas as pd
from uuid import UUID

from .CrudApi import CrudApi
from .AuthApi import Auth

# sys.path.insert(0, f"{sys.path[0]}/..")
from ..Dto.ExchangeDto import ExchangeDto
from ..Dto.PagedAndSortedResultRequestDto import PagedAndSortedResultRequestDto
from ..Dto.CreateUpdateExchangeDto import *


class ExchangeApi(
    CrudApi[
        UUID,
        ExchangeDto,
        PagedAndSortedResultRequestDto,
        CreateUpdateExchangeDto,
        CreateUpdateExchangeDto,
    ]
):
    """
    Exchange API for performing CRUD operations on exchanges.

        from sparks.ApiClient import ApiClient

        api = ApiClient()
        login = api.Login("admin", "1q2w3E*")
        print(f"Login:{login}")

        # get exchanges list
        df = api.Exchange.GetList()
        print(df)
    """

    def __init__(self, apiUrl: str, accessToken: str) -> None:
        CrudApi.__init__(self, apiUrl, accessToken, "app/exchange", ExchangeDto)


## from sparks import config as cfg
# from .. import config as cfg
#
# if __name__ == "__main__":
#    auth = Auth()
#    cfg.AccessToken = auth.GetAccessToken(cfg.AuthTokenUrl, cfg.Auth_Info)
#    print(cfg.AccessToken)
#
#    exchanges = ExchangeApi(cfg.AccessToken)
#    # df = exchanges.Get("3a0e534b-6fc9-93c9-b8e1-f6919567e8ea")
#    # df = exchanges.GetList()
#    # df = exchanges.GetList(PagedAndSortedResultRequestDto(maxResultCount=2))
#
#    createDto = CreateUpdateExchangeDto(
#        code="test",
#        name="test",
#        district=EDistrict.CN,
#        currency=ECurrency.CNY,
#        iconPath="",
#    )
#    df = exchanges.Create(createDto)
#    print(df)
#
#    createDto = CreateUpdateExchangeDto(
#        code="test2",
#        name="test2",
#        district=EDistrict.CN,
#        currency=ECurrency.CNY,
#        iconPath="",
#    )
#    df = exchanges.Update(df.id, createDto)
#    # print(df.dtypes)
#    print(df)
#
#    r = exchanges.Delete(df.id)
#    # print(df.dtypes)
#    print(f"Delete {df.id} :{r}")
