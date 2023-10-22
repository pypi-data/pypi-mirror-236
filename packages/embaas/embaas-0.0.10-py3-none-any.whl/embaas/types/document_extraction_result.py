

import datetime as dt
import typing

import pydantic

from .document_chunk import DocumentChunk
from ..core.datetime_utils import serialize_datetime


class DocumentExtractionResult(pydantic.BaseModel):
    chunks: typing.List[DocumentChunk]
    metadata: typing.Dict[str, typing.Any]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
