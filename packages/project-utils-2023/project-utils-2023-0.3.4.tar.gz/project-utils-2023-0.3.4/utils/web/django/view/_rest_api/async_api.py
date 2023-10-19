from abc import ABCMeta, abstractmethod

from rest_framework.request import Request

from utils.exception import DjangoWebException, ViewException
from utils.web.django import WebRequest, WebResponse
from utils.web.django.conf import DjangoConfig

from .api_utils import BaseRestAPI
from .._async_view import AsyncAPIView


class AsyncRestApi(AsyncAPIView, metaclass=ABCMeta):
    config: DjangoConfig

    async def initialize_request(self, request, *args, **kwargs):
        request: Request = await super().initialize_request(request, *args, **kwargs)
        api_util: BaseRestAPI = BaseRestAPI(request, method=request.method, config=self.config)
        web_request: WebRequest = api_util.request_init(self.config)
        return web_request

    async def show_exception(self, e: DjangoWebException):
        self.config.printf.error(e.error_detail)
        self.config.printf.warning(e.error_summary)

    async def create_exception(self, status: int, e: Exception) -> ViewException:
        return ViewException(status=status, error_summary=str(e), error_detail=traceback.format_exc())

    def initial(self, request, *args, **kwargs):
        self.request = request.request
        return super().initial(request.request)

    def finalize_response(self, request, response, *args, **kwargs):
        request: WebRequest = request
        response: WebResponse = response
        return super().finalize_response(request, response.to_rest_response())
