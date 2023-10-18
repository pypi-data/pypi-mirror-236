import asyncio
import traceback

from typing import Union

from asgiref.sync import async_to_sync

from rest_framework.request import Request
from rest_framework.response import Response

from utils.exception import ViewException
from utils.web.django.conf import DjangoConfig
from utils.web.django.request import WebRequest
from utils.web.django.response import WebResponse

from .api_util import BaseRestAPI

from .._types import REST_API_TYPE, VIEW_TYPE, REST_VIEW_HANDLER_TYPE


def rest_api(method: str = "get") -> REST_API_TYPE:
    def decorator(fun: VIEW_TYPE) -> REST_VIEW_HANDLER_TYPE:
        def handler(request: Union[Request, WebRequest], *args: ..., **kwargs: ...) -> Response:
            if type(request) == WebRequest:
                request = request.request
            config: DjangoConfig = request.config
            base_rest_api: BaseRestAPI = BaseRestAPI(request, method, config)
            try:
                web_request: WebRequest = base_rest_api.request_init(config)
            except ViewException as e:
                config.printf.warning(e.error_summary)
                config.printf.error(e.error_detail)
                return WebResponse(status=e.status, error=e).to_rest_response()
            except Exception as e:
                e_ = ViewException(403, str(e), traceback.format_exc())
                config.printf.error(e_.error_detail)
                config.printf.warning(e_.error_summary)
                return WebResponse(status=e_.status, error=e_).to_rest_response()
            try:
                if asyncio.iscoroutinefunction(fun):
                    web_response: Union[Response, WebResponse] = async_to_sync(fun)(web_request, *args, **kwargs)
                else:
                    web_response: Union[Response, WebResponse] = fun(web_request, *args, **kwargs)
                if type(web_response) == Response:
                    return web_response
                else:
                    return web_response.to_rest_response()
            except ViewException as e:
                config.printf.error(e.error_detail)
                config.printf.warning(e.error_summary)
                return WebResponse(e.status, error=e).to_rest_response()
            except Exception as e:
                e_ = ViewException(410, str(e), traceback.format_exc())
                config.printf.error(e_.error_detail)
                config.printf.warning(e_.error_summary)
                return WebResponse(status=e_.status, error=e_).to_rest_response()

        return handler

    return decorator
