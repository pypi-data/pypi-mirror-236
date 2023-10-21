from .BaseApi import BaseApi
import pandas as pd
from uuid import UUID
import sys

from typing import TypeVar, Generic
from pydantic import BaseModel

TEntityDto = TypeVar("TEntityDto", bound=BaseModel)
TCreateInput = TypeVar("TCreateInput", bound=BaseModel)
TUpdateInput = TypeVar("TUpdateInput", bound=BaseModel)
TGetListInput = TypeVar("TGetListInput", bound=BaseModel)
TKey = TypeVar("TKey", bound=UUID)


class CrudApi(
    Generic[
        TKey,
        TEntityDto,
        TGetListInput,
        TCreateInput,
        TUpdateInput,
    ],
    BaseApi,
):
    """
    Login indicate if logined.
    """

    _TEntityDto: type  # 因为typevar在运行时其实并不存在，需要在init的时候提供一个type变量，以用于instantiate

    def __init__(
        self, apiUrl: str, accessToken: str, endpoint: str, tEntityDto: type
    ) -> None:
        BaseApi.__init__(self, apiUrl, accessToken)
        self.endpoint = endpoint
        self._TEntityDto = tEntityDto

    def Get(self, id: TKey) -> TEntityDto:
        """
        Get the entity with the specified ID.

        Args:
            id: The ID of the entity.

        Returns:
            TEntityDto: The entity object.

        Raises:
            None.

        Examples:
            >>> api = CrudApi()
            >>> entity = api.Get(1)
        """
        r = self._rest_get_method(endpoint=self.endpoint, uri=id)
        # print(type(r))
        # print(r)
        return self._TEntityDto(**r)

    def GetList(self, dto: TGetListInput = None) -> pd.DataFrame:
        params = dto.model_dump() if dto is not None else None
        print(params)
        r = self._rest_get_method(endpoint=self.endpoint, params=params)
        l = r["items"]
        df = pd.DataFrame(l)
        # from_list(ExchangeDto.from_dict, r.get("ExchangeDto"))
        print(type(r))
        print(r)
        return df

    def Create(self, dto: TCreateInput) -> TEntityDto:
        json = dto.model_dump() if dto is not None else None
        # print(req.model_dump())
        r = self._rest_post_method(endpoint=self.endpoint, json=json)
        print(type(r))
        print(r)

        r = self._TEntityDto(**r)
        return r

    def Update(self, id: TKey, dto: TUpdateInput) -> TEntityDto:
        json = dto.model_dump() if dto is not None else None
        # print(req.model_dump())
        r = self._rest_put_method(endpoint=self.endpoint, uri=id, json=json)
        print(type(r))
        print(r)

        r = self._TEntityDto(**r)
        return r

    def Delete(self, id: TKey) -> bool:
        return self._rest_delete_method(endpoint=self.endpoint, uri=id)
