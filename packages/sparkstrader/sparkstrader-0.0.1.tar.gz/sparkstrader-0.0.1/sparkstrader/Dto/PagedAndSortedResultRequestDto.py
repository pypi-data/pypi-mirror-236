from typing import Optional
from pydantic import BaseModel, Field


class PagedAndSortedResultRequestDto(BaseModel):
    sorting: Optional[str] = None
    skipCount: Optional[int] = None
    maxResultCount: Optional[int] = None
