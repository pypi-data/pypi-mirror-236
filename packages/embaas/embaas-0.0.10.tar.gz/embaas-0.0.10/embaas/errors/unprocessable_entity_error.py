

from .api_error import ApiError
from ..types.http_validation_error import HttpValidationError


class UnprocessableEntityError(ApiError):
    def __init__(self, body: HttpValidationError):
        super().__init__(status_code=422, body=body)
