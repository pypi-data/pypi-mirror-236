

import datetime as dt
import typing

import pydantic

from .embedding import Embedding
from .usage import Usage
from ..core.datetime_utils import serialize_datetime


class EmbeddingsResponse(pydantic.BaseModel):
    usage: Usage
    model: str
    data: typing.List[Embedding]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
