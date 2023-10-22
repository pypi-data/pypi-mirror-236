from datetime import datetime
from typing import List

from pydantic import BaseModel, Extra, Field
from pydantic.v1 import BaseModel as BaseModelV1


class DetailResponseDto(BaseModelV1):
    loc: List[str]
    msg: str
    type: str


class ExceptionResponseDto(BaseModelV1):
    detail: List[DetailResponseDto]
    status_code: int = 422
    timestamp: datetime
    path: str
    method: str

    class Config:
        extra = Extra.forbid
