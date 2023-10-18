from ._base_view import BaseRestAPIView
from ._async_view import AsyncAPIView
from ._async_base_view import AsyncBaseAPIView
from ._swagger_base import SwaggerTypeBase

BaseView = RestAPIView = RestView = BaseRestAPIView
AsyncView = AsyncAPIView
AsyncBaseView = AsyncBaseAPIView
SwaggerType = SwaggerTypeBase

__all__ = [
    "BaseView",
    "RestAPIView",
    "RestView",
    "BaseRestAPIView",
    "AsyncView",
    "AsyncAPIView",
    "AsyncBaseView",
    "AsyncBaseAPIView",
    "SwaggerType",
    "SwaggerTypeBase"
]
