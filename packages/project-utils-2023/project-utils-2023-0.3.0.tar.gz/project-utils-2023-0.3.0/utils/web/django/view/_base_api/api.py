import traceback
import functools

from loguru._logger import Logger

from django.http.request import HttpRequest
from django.http.response import HttpResponse

from utils.exception import ViewException
from utils.web.django.conf import DjangoConfig
from utils.web.django.request import WebRequest
from utils.web.django.response import WebResponse

from .api_util import BaseAPIUtil

from .._types import BASE_API_TYPE, VIEW_TYPE, API_VIEW_HANDLER_TYPE


def base_api(config: DjangoConfig, method: str = "get") -> BASE_API_TYPE:
    def decorator(fun: VIEW_TYPE) -> API_VIEW_HANDLER_TYPE:
        def handler(request: HttpRequest, *args: ..., **kwargs: ...) -> HttpResponse:
            try:
                api_util: BaseAPIUtil = BaseAPIUtil(config=config, request=request, method=method)
            except ViewException as e:
                config.printf.error(e.error_detail)
                config.printf.warning(e.error_summary)
                return WebResponse(status=e.status, error=e).to_response()
            except Exception as e:
                view_exception: ViewException = ViewException(405, str(e), traceback.format_exc())
                config.printf.error(view_exception.error_detail)
                config.printf.warning(view_exception.error_summary)
                return WebResponse(status=view_exception.status, error=view_exception).to_response()
            try:
                web_request: WebRequest = api_util.request_init(config)
            except ViewException as e:
                config.printf.error(e.error_detail)
                config.printf.warning(e.error_summary)
                return WebResponse(status=e.status, error=e).to_response()
            except Exception as e:
                view_exception: ViewException = ViewException(403, str(e), traceback.format_exc())
                config.printf.error(view_exception.error_detail)
                config.printf.warning(view_exception.error_summary)
                return WebResponse(status=view_exception.status, error=view_exception).to_response()
            try:
                web_response: WebResponse = fun(web_request, *args, **kwargs)
            except ViewException as e:
                config.printf.error(e.error_detail)
                config.printf.warning(e.error_summary)
                return WebResponse(status=e.status, error=e).to_response()
            except Exception as e:
                view_exception: ViewException = ViewException(410, str(e), traceback.format_exc())
                config.printf.error(view_exception.error_detail)
                config.printf.warning(view_exception.error_summary)
                return WebResponse(status=view_exception.status, error=view_exception).to_response()
            return web_response.to_response()

        return handler

    return decorator


def async_base_api(config: DjangoConfig, method: str = "get"):
    printf: Logger = config.printf

    def decorator(fun):
        def handler(request, *args, **kwargs):
            async def inner(request, *args, **kwargs):
                try:
                    api_util: BaseAPIUtil = BaseAPIUtil(request, method, config=config)
                except ViewException as e:
                    printf.error(e.error_detail)
                    printf.warning(e.error_summary)
                    return WebResponse(status=e.status, error=e).to_response()
                except Exception as e:
                    e_ = ViewException(405, str(e), traceback.format_exc())
                    printf.error(e_.error_detail)
                    printf.warning(e_.error_summary)
                    return WebResponse(status=e_.status, error=e_).to_response()
                try:
                    web_request: WebRequest = await api_util.async_request_init(config)
                except ViewException as e:
                    printf.warning(e.error_summary)
                    printf.error(e.error_detail)
                    return WebResponse(status=e.status, error=e).to_response()
                except Exception as e:
                    e_ = ViewException(403, str(e), traceback.format_exc())
                    printf.error(e_.error_detail)
                    printf.warning(e_.error_summary)
                    return WebResponse(status=e_.status, error=e_).to_response()
                try:
                    web_response: WebResponse = await fun(web_request, *args, **kwargs)
                except ViewException as e:
                    printf.warning(e.error_summary)
                    printf.error(e.error_detail)
                    return WebResponse(status=e.status, error=e).to_response()
                except Exception as e:
                    e_ = ViewException(410, str(e), traceback.format_exc())
                    printf.error(e_.error_detail)
                    printf.warning(e_.error_summary)
                    return WebResponse(status=e_.status, error=e_).to_response()
                return web_response.to_response()

            return config.loop.run_until_complete(inner(request, *args, **kwargs))

        return handler

    return decorator
