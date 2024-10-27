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


def calculate_age(date_visit, date_birth):
    """
    Calculate the age from date_birth to date_visit.
    Returns a string in the format 'Xг Yм Zд'.
    """
    # Вытаскиваем дату посещения и дату рождения как объекты datetime
    if isinstance(date_visit, str):
        visit_date = datetime.fromisoformat(date_visit)
    else:
        visit_date = date_visit

    if isinstance(date_birth, str):
        birth_date = datetime.fromisoformat(date_birth)
    else:
        birth_date = date_birth

    # Вычисление разницы
    years = visit_date.year - birth_date.year
    months = visit_date.month - birth_date.month
    days = visit_date.day - birth_date.day

    # Коррекция при отрицательных значениях
    if days < 0:
        months -= 1
        last_month = (visit_date.month - 1) if visit_date.month > 1 else 12
        days += (birth_date.replace(year=birth_date.year + (1 if last_month == 12 else 0),
                                    month=last_month) - birth_date).days

    if months < 0:
        years -= 1
        months += 12

    return f"{years}г {months}м {days}д"
