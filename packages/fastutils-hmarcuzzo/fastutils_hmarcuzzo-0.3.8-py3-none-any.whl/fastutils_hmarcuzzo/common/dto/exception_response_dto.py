from datetime import datetime
from typing import List

from pydantic import BaseModel, Extra, Field
from pydantic.v1 import BaseModel as BaseModelV1


class DetailResponseDto(BaseModel):
    loc: List[str] = Field(title="Location")
    msg: str = Field(title="Message")
    type: str = Field(title="Error Type")


class ExceptionResponseDto(BaseModelV1):
    detail: List[DetailResponseDto]
    status_code: int = 422
    timestamp: datetime = Field(title="Timestamp of the Request")
    path: str = Field(title="Request Path")
    method: str = Field(title="Request Method")

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.forbid
