from starlette.responses import PlainTextResponse

from utils.responses import Http400, Http500, Http404


async def unicorn_exception_handler(request, exc):
    """Отслеживание исключений HTTPException на уровне
    обработчиков роутов приложения FastAPI.

    Использование:
    ::
        from starlette.exceptions import HTTPException as StarletteHTTPException
        from inm_core.utils import unicorn_exception_handler

        def create_app():
            app = FastApi()
            app.exception_handler(StarletteHTTPException)(unicorn_exception_handler)
            return app

    :param request: HTTP-запрос FastAPI.Request.
    :param exc: Исключение HTTPException.
    :return: Стандартный ответ.
    """

    match exc.status_code:
        case 400:
            return Http400(exc.detail).get_response()
        case 404:
            return Http404().get_response()
        case 500:
            return Http500(str(exc.detail)).get_response()
        case _:
            return PlainTextResponse(status_code=exc.status_code, content=str(exc.detail))


async def global_exception_handling(request, call_next):
    """Отслеживание исключений при обработке HTTP-запросов на уровне Middleware.

    Использование:
    ::
        from inm_core.utils import global_exception_handling

        def create_app():
            app = FastApi()
            app.middleware("http")(global_exception_handling)
            return app

    :param request: HTTP-запрос FastAPI.Request.
    :param call_next: Метод для обработки HTTP-запроса.
    :return: Стандартный ответ.
    """

    try:
        return await call_next(request)
    except Exception as e:
        return Http500(str(e)).get_response()


