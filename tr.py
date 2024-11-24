from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from pydantic_i18n import PydanticI18n

# Параметры локализации
DEFAULT_LOCALE = "ru_RU"  # Устанавливаем русский язык по умолчанию

translations = {
    "ru_RU": {
        "Field required": "Поле {field} обязательное",
        "String should have at least {} character": "Поле {{field}} не может быть меньше {} символов",
        "String should have at most {} characters": "Поле {{field}} не может быть больше {} символов",
        "string_length": "Длина строки должна быть не менее {min_length} символов",
        "Input should be a valid integer, unable to parse string as an integer": "Поле {field} должно быть числом",
        "Input should be less than or equal to {}": "Поле {{field}} должно быть не больше {}",
        "Input should be greater than or equal to {}": "Поле {{field}} должно быть не меньше {}"
    },
    "en_US": {
        "Field required": "-",
        "String should have at least {} character": "-",
        "String should have at most {} characters": "-",
        "string_length": "-",
        "Input should be a valid integer, unable to parse string as an integer": "-",
        "Input should be less than or equal to {}": "-",
        "Input should be greater than or equal to {}": "-"
    },
    "de_DE": {
        "Field required": "-",
        "String should have at least {} character": "-",
        "String should have at most {} characters": "-",
        "string_length": "-",
        "Input should be a valid integer, unable to parse string as an integer": "-",
        "Input should be less than or equal to {}": "-",
        "Input should be greater than or equal to {}": "-"
    },
}

tr = PydanticI18n(translations)


def get_locale(locale: str = DEFAULT_LOCALE) -> str:
    return locale


import logging


async def validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> JSONResponse:
    current_locale = request.query_params.get("locale", DEFAULT_LOCALE)

    # Получаем переведённые ошибки
    errors = tr.translate(exc.errors(), current_locale)
    formatted_errors = []

    # Обрабатываем ошибки
    for error in errors:
        logging.error(error["msg"])
        logging.error(error["loc"][1])
        error_message = error["msg"].replace("{field}", error["loc"][1])
        formatted_errors.append(error_message)

    return JSONResponse({"response": {"errors": formatted_errors}}, 400)


# Обратите внимание на то, присутствует ли import-all для вашего модуля
__all__ = ["get_locale", "validation_exception_handler"]
