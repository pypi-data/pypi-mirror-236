import traceback

from typing import Union

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


def async_rest_api(method: str = "get"):
    def decorator(fun):
        def handler(request: Union[Request, WebRequest], *args: ..., **kwargs: ...):
            if type(request) == WebRequest:
                request = request.request

            async def inner(request, *args, **kwargs):
                config: DjangoConfig = request.config
                base_rest_api: BaseRestAPI = BaseRestAPI(request, method, config)
                try:
                    web_request: WebRequest = await base_rest_api.async_request_init(config)
                except ViewException as e:
                    config.printf.error(e.error_detail)
                    config.printf.warning(e.error_summary)
                    return WebResponse(status=e.status, error=e).to_rest_response()
                except Exception as e:
                    exception: ViewException = ViewException(403, str(e), traceback.format_exc())
                    config.printf.error(exception.error_detail)
                    config.printf.warning(exception.error_summary)
                    return WebResponse(status=exception.status, error=exception)
                try:
                    web_response: Union[Response, WebResponse] = await fun(web_request, *args, **kwargs)
                    if type(web_response) == Response:
                        return web_response
                    else:
                        return web_response.to_rest_response()
                except ViewException as e:
                    config.printf.error(e.error_detail)
                    config.printf.warning(e.error_summary)
                    return WebResponse(status=e.status, error=e).to_rest_response()
                except Exception as e:
                    _e: ViewException = ViewException(410, str(e), traceback.format_exc())
                    config.printf.error(_e.error_detail)
                    config.printf.warning(_e.error_summary)
                    return WebResponse(status=410, error=_e).to_rest_response()

            return request.config.loop.run_until_complete(inner(request, *args, **kwargs))

        return handler

    return decorator
