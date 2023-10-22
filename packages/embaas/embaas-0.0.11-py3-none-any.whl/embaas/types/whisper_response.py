

import datetime as dt
import typing

import pydantic

from .whisper_result import WhisperResult
from .whisper_usage import WhisperUsage
from ..core.datetime_utils import serialize_datetime


class WhisperResponse(pydantic.BaseModel):
    data: typing.List[WhisperResult]
    usage: WhisperUsage
    model: str

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
