from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field
from sparkstrader.Enums.Enums import *
from datetime import datetime
from uuid import UUID


class ExchangeDto(BaseModel):
    code: str
    name: str
    district: EDistrict
    currency: ECurrency
    iconPath: Optional[str]
    isDeleted: bool
    deleterId: UUID | None
    deletionTime: datetime | None
    lastModificationTime: datetime | None
    lastModifierId: UUID | None
    creationTime: datetime | None
    creatorId: UUID | None
    id: UUID
