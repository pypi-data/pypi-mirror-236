

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime


class DocumentChunk(pydantic.BaseModel):
    text: str
    metadata: typing.Dict[str, typing.Any]
    embedding: typing.Optional[typing.List[float]] = None
    index: int

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
