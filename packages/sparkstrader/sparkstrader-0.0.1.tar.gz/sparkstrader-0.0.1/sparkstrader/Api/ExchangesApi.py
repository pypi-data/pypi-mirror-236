from BaseApi import BaseApi
from AuthApi import Auth
import pandas as pd
from uuid import UUID
import sys

import config as cfg

# sys.path.insert(0, f"{sys.path[0]}/..")
from Dto.ExchangeDto import ExchangeDto
from Dto.PagedAndSortedResultRequestDto import PagedAndSortedResultRequestDto
from Dto.CreateUpdateExchangeDto import *


class Exchanges(BaseApi):
    def __init__(self, accessToken: str) -> None:
        super(Exchanges, self).__init__(accessToken)
        self.endpoint = "app/exchange"

    def Get(self, id: UUID) -> ExchangeDto:
        r = self._rest_get_method(endpoint=self.endpoint, uri=id)
        # print(type(r))
        # print(r)
        return ExchangeDto(**r)

    def GetList(self, dto: PagedAndSortedResultRequestDto = None) -> pd.DataFrame:
        params = dto.model_dump() if dto is not None else None
        print(params)
        r = self._rest_get_method(endpoint=self.endpoint, params=params)
        l = r["items"]
        df = pd.DataFrame(l)
        # from_list(ExchangeDto.from_dict, r.get("ExchangeDto"))
        print(type(r))
        print(r)
        return df

    def Create(self, dto: CreateUpdateExchangeDto) -> ExchangeDto:
        json = dto.model_dump() if dto is not None else None
        # print(req.model_dump())
        r = self._rest_post_method(endpoint=self.endpoint, json=json)
        print(type(r))
        print(r)

        r = ExchangeDto(**r)
        return r

    def Update(self, id: UUID, dto: CreateUpdateExchangeDto) -> ExchangeDto:
        json = dto.model_dump() if dto is not None else None
        # print(req.model_dump())
        r = self._rest_put_method(endpoint=self.endpoint, uri=id, json=json)
        print(type(r))
        print(r)

        r = ExchangeDto(**r)
        return r

    def Delete(self, id: UUID) -> bool:
        return self._rest_delete_method(endpoint=self.endpoint, uri=id)


# sys.path.insert(0, f"{sys.path[0]}/../../")
import config as cfg


if __name__ == "__main__":
    auth = Auth()
    cfg.AccessToken = auth.GetAccessToken(cfg.AuthTokenUrl, cfg.Auth_Info)
    print(cfg.AccessToken)

    exchanges = Exchanges(cfg.AccessToken)
    # df = exchanges.Get("3a0e534b-6fc9-93c9-b8e1-f6919567e8ea")
    # df = exchanges.GetList()
    # df = exchanges.GetList(PagedAndSortedResultRequestDto(maxResultCount=2))

    createDto = CreateUpdateExchangeDto(
        code="test",
        name="test",
        district=EDistrict.CN,
        currency=ECurrency.CNY,
        iconPath="",
    )
    df = exchanges.Create(createDto)
    print(df)

    createDto = CreateUpdateExchangeDto(
        code="test2",
        name="test2",
        district=EDistrict.CN,
        currency=ECurrency.CNY,
        iconPath="",
    )
    df = exchanges.Update(df.id, createDto)
    # print(df.dtypes)
    print(df)

    r = exchanges.Delete(df.id)
    # print(df.dtypes)
    print(f"Delete {df.id} :{r}")
