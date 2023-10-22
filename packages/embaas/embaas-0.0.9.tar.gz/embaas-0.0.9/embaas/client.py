import abc
import base64
import typing
import urllib.parse
from json.decoder import JSONDecodeError

import httpx
from pydantic import BaseModel, root_validator, Field

from .core import remove_none_from_headers
from .errors import ApiError, UnprocessableEntityError
from .utils import get_from_dict_or_env
from .types import DocumentExtractionResponseWithEmbeddings, DocumentExtractionResponse, EmbeddingsResponse, \
    DocumentByteTextExtractionResponse, DocumentFileTextExtractionResponse, WhisperResponse, ChunkSplitter

OMIT = typing.cast(typing.Any, ...)
T = typing.TypeVar("T", bound=BaseModel)
DEFAULT_ENVIRONMENT = "https://api.embaas.io"
DEFAULT_MODEL = "e5-large-v2"


class SendRequestMixin(abc.ABC):
    @abc.abstractmethod
    def send_request(
            self,
            method: str,
            endpoint: str,
            response_model: typing.Type[T],
            request_data: typing.Dict[str, typing.Any] = OMIT,
            files: typing.Dict[str, typing.Any] = OMIT,
            headers: typing.Dict[str, typing.Any] = {},
    ) -> T:
        ...

    def get_request_kwargs(
            self,
            method: str,
            endpoint: str,
            headers: typing.Dict[str, typing.Any] = {},
            files: typing.Dict[str, typing.Any] = OMIT,
            request_data: typing.Dict[str, typing.Any] = OMIT,
    ) -> dict:
        url = urllib.parse.urljoin(self.environment, endpoint)
        cleaned_request_data = {}
        for key, value in request_data.items():
            if value is not OMIT:
                cleaned_request_data[key] = value

        request_kwargs = {
            "method": method,
            "url": url,
            "headers": remove_none_from_headers({"Authorization": self.api_key, **headers}),
        }

        if files is not OMIT:
            request_kwargs["files"] = files
            request_kwargs["data"] = cleaned_request_data
        else:
            request_kwargs["json"] = cleaned_request_data

        return request_kwargs

    def handle_response(self, response: httpx.Response, response_model: typing.Type[T]) -> T:
        try:
            if 200 <= response.status_code < 300:
                return response_model.parse_obj(response.json())
            if response.status_code == 422:
                raise UnprocessableEntityError(response.json())
        except JSONDecodeError:
            raise ApiError(status_code=response.status_code, body=response.text)

        raise ApiError(status_code=response.status_code, body=response.json())


class BaseEmbaasClient(BaseModel, SendRequestMixin):
    api_key: str
    environment: str = DEFAULT_ENVIRONMENT
    request_timeout: int = Field(default=180, ge=1)

    @root_validator(pre=True)
    def validate_environment(cls, values: typing.Dict) -> typing.Dict:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "EMBAAS_API_KEY")
        return values

    @abc.abstractmethod
    def get_embeddings(
            self, *, model: str, texts: typing.List[str], instruction: typing.Optional[str] = OMIT
    ) -> EmbeddingsResponse:
        pass

    @abc.abstractmethod
    def extract_text_from_file(
            self,
            *,
            file: typing.IO,
            should_chunk: typing.Optional[bool] = OMIT,
            chunk_size: typing.Optional[int] = OMIT,
            chunk_overlap: typing.Optional[int] = OMIT,
            chunk_splitter: typing.Optional[ChunkSplitter] = OMIT,
            separators: typing.Optional[typing.List[str]] = OMIT,
            should_embed: typing.Optional[bool] = OMIT,
            model: typing.Optional[str] = OMIT,
            instruction: typing.Optional[str] = OMIT,
    ) -> DocumentFileTextExtractionResponse:
        pass

    @abc.abstractmethod
    def extract_text_from_bytes(
            self,
            *,
            bytes_or_base64: typing.Union[bytes, str],
            file_name: typing.Optional[str] = OMIT,
            mime_type: typing.Optional[str] = OMIT,
            file_extension: typing.Optional[str] = OMIT,
            should_chunk: typing.Optional[bool] = OMIT,
            chunk_size: typing.Optional[int] = OMIT,
            chunk_overlap: typing.Optional[int] = OMIT,
            chunk_splitter: typing.Optional[ChunkSplitter] = OMIT,
            separators: typing.Optional[typing.List[str]] = OMIT,
            should_embed: typing.Optional[bool] = OMIT,
            model: typing.Optional[str] = OMIT,
            instruction: typing.Optional[str] = OMIT,
    ) -> DocumentByteTextExtractionResponse:
        pass

    @abc.abstractmethod
    def transcribe(self, *, file: typing.IO) -> WhisperResponse:
        pass


class EmbaasClient(BaseEmbaasClient):
    def send_request(
            self,
            method: str,
            endpoint: str,
            response_model: typing.Type[T],
            request_data: typing.Dict[str, typing.Any] = OMIT,
            files: typing.Dict[str, typing.Any] = OMIT,
            headers: typing.Dict[str, typing.Any] = {},
    ) -> T:
        request_kwargs = self.get_request_kwargs(method=method,
                                                 endpoint=endpoint,
                                                 headers=headers,
                                                 files=files,
                                                 request_data=request_data)
        with httpx.Client(timeout=self.request_timeout) as client:
            response = client.request(**request_kwargs)
        return self.handle_response(response, response_model)

    def get_embeddings(
            self, *, model: str = DEFAULT_MODEL, texts: typing.List[str], instruction: typing.Optional[str] = OMIT
    ) -> EmbeddingsResponse:
        request_data: typing.Dict[str, typing.Any] = {"model": model, "texts": texts, "instruction": instruction}

        return self.send_request(
            "POST",
            "v1/embeddings/",
            EmbeddingsResponse,
            request_data
        )

    def extract_text_from_file(
            self,
            *,
            file: typing.IO,
            should_chunk: typing.Optional[bool] = OMIT,
            chunk_size: typing.Optional[int] = OMIT,
            chunk_overlap: typing.Optional[int] = OMIT,
            chunk_splitter: typing.Optional[ChunkSplitter] = OMIT,
            separators: typing.Optional[typing.List[str]] = OMIT,
            should_embed: typing.Optional[bool] = OMIT,
            model: typing.Optional[str] = OMIT,
            instruction: typing.Optional[str] = OMIT,
    ) -> DocumentFileTextExtractionResponse:
        request_data: typing.Dict[str, typing.Any] = {
            "should_chunk": should_chunk,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "chunk_splitter": chunk_splitter.value if chunk_splitter is not OMIT else OMIT,
            "separators": separators,
            "should_embed": should_embed,
            "model": model,
            "instruction": instruction,
        }
        files = {"file": file}

        return self.send_request(
            "POST",
            "v1/document/extract-text/",
            DocumentExtractionResponseWithEmbeddings if should_embed is True else DocumentExtractionResponse,
            request_data=request_data,
            files=files,
        )

    def extract_text_from_bytes(
            self,
            *,
            bytes_or_base64: typing.Union[bytes, str],
            file_name: typing.Optional[str] = OMIT,
            mime_type: typing.Optional[str] = OMIT,
            file_extension: typing.Optional[str] = OMIT,
            should_chunk: typing.Optional[bool] = OMIT,
            chunk_size: typing.Optional[int] = OMIT,
            chunk_overlap: typing.Optional[int] = OMIT,
            chunk_splitter: typing.Optional[ChunkSplitter] = OMIT,
            separators: typing.Optional[typing.List[str]] = OMIT,
            should_embed: typing.Optional[bool] = OMIT,
            model: typing.Optional[str] = OMIT,
            instruction: typing.Optional[str] = OMIT,
    ) -> DocumentByteTextExtractionResponse:
        request_data: typing.Dict[str, typing.Any] = {
            "should_chunk": should_chunk,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "chunk_splitter": chunk_splitter.value if chunk_splitter is not OMIT else OMIT,
            "separators": separators,
            "should_embed": should_embed,
            "model": model,
            "instruction": instruction,
            "bytes": base64.b64encode(bytes_or_base64).decode() if isinstance(bytes_or_base64,
                                                                              bytes) else bytes_or_base64,
            "file_name": file_name,
            "mime_type": mime_type,
            "file_extension": file_extension,
        }

        return self.send_request(
            "POST",
            "v1/document/extract-text/bytes/",
            DocumentExtractionResponseWithEmbeddings if should_embed is True else DocumentExtractionResponse,
            request_data=request_data,
        )

    def transcribe(self, *, file: typing.IO) -> WhisperResponse:
        files = {"file": file}

        return self.send_request(
            "POST",
            "v1/whisper/",
            WhisperResponse,
            files=files,
        )


class EmbaasAsyncClient(BaseEmbaasClient):
    async def send_request(
            self,
            method: str,
            endpoint: str,
            response_model: typing.Type[T],
            request_data: typing.Dict[str, typing.Any] = OMIT,
            files: typing.Dict[str, typing.Any] = OMIT,
            headers: typing.Dict[str, typing.Any] = {},
    ) -> T:
        request_kwargs = self.get_request_kwargs(method=method,
                                                 endpoint=endpoint,
                                                 headers=headers,
                                                 files=files,
                                                 request_data=request_data)
        async with httpx.AsyncClient(timeout=self.request_timeout) as client:
            response = await client.request(**request_kwargs)
        return self.handle_response(response, response_model)

    async def get_embeddings(
            self, *, model: str, texts: typing.List[str], instruction: typing.Optional[str] = OMIT
    ) -> EmbeddingsResponse:
        request_data: typing.Dict[str, typing.Any] = {"model": model, "texts": texts, "instruction": instruction}

        return await self.send_request(
            "POST",
            "v1/embeddings/",
            EmbeddingsResponse,
            request_data
        )

    async def extract_text_from_file(
            self,
            *,
            file: typing.IO,
            should_chunk: typing.Optional[bool] = OMIT,
            chunk_size: typing.Optional[int] = OMIT,
            chunk_overlap: typing.Optional[int] = OMIT,
            chunk_splitter: typing.Optional[ChunkSplitter] = OMIT,
            separators: typing.Optional[typing.List[str]] = OMIT,
            should_embed: typing.Optional[bool] = OMIT,
            model: typing.Optional[str] = OMIT,
            instruction: typing.Optional[str] = OMIT,
    ) -> DocumentFileTextExtractionResponse:
        request_data: typing.Dict[str, typing.Any] = {
            "should_chunk": should_chunk,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "chunk_splitter": chunk_splitter.value if chunk_splitter is not OMIT else OMIT,
            "separators": separators,
            "should_embed": should_embed,
            "model": model,
            "instruction": instruction,
        }
        files = {"file": file}

        return await self.send_request(
            "POST",
            "v1/document/extract-text/",
            DocumentExtractionResponseWithEmbeddings if should_embed is True else DocumentExtractionResponse,
            request_data=request_data,
            files=files,
        )

    async def extract_text_from_bytes(
            self,
            *,
            bytes_or_base64: typing.Union[bytes, str],
            file_name: typing.Optional[str] = OMIT,
            mime_type: typing.Optional[str] = OMIT,
            file_extension: typing.Optional[str] = OMIT,
            should_chunk: typing.Optional[bool] = OMIT,
            chunk_size: typing.Optional[int] = OMIT,
            chunk_overlap: typing.Optional[int] = OMIT,
            chunk_splitter: typing.Optional[ChunkSplitter] = OMIT,
            separators: typing.Optional[typing.List[str]] = OMIT,
            should_embed: typing.Optional[bool] = OMIT,
            model: typing.Optional[str] = OMIT,
            instruction: typing.Optional[str] = OMIT,
    ) -> DocumentByteTextExtractionResponse:
        request_data: typing.Dict[str, typing.Any] = {
            "should_chunk": should_chunk,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "chunk_splitter": chunk_splitter.value if chunk_splitter is not OMIT else OMIT,
            "separators": separators,
            "should_embed": should_embed,
            "model": model,
            "instruction": instruction,
            "bytes": base64.b64encode(bytes_or_base64).decode() if isinstance(bytes_or_base64,
                                                                              bytes) else bytes_or_base64,
            "file_name": file_name,
            "mime_type": mime_type,
            "file_extension": file_extension,
        }

        return await self.send_request(
            "POST",
            "v1/document/extract-text/bytes/",
            DocumentExtractionResponseWithEmbeddings if should_embed is True else DocumentExtractionResponse,
            request_data=request_data,
        )

    async def transcribe(self, *, file: typing.IO) -> WhisperResponse:
        files = {"file": file}

        return await self.send_request(
            "POST",
            "v1/whisper/",
            WhisperResponse,
            files=files,
        )
