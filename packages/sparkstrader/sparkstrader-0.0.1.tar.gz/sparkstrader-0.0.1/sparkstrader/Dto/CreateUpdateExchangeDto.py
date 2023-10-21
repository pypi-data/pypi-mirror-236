from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field
from sparkstrader.Enums.Enums import *


# @dataclass
class CreateUpdateExchangeDto(BaseModel):
    code: str = Field(..., min_length=1, max_length=32)
    name: str = Field(..., max_length=128)
    district: EDistrict
    currency: ECurrency
    iconPath: Optional[str] = Field(None, max_length=256)
