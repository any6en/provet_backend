from datetime import datetime


def format_date_dmy_dt(date_string: str, is_need_time: bool = False, is_month_translate: bool = False) -> str or list:
    # Парсинг строки даты
    date = datetime.fromisoformat(date_string)

    # Получение деталей даты
    day = str(date.day).zfill(2)  # День с ведущим нулем
    year = date.year

    # Названия месяцев на русском
    months_in_russian = [
        'января', 'февраля', 'марта', 'апреля', 'мая',
        'июня', 'июля', 'августа', 'сентября', 'октября',
        'ноября', 'декабря'
    ]

    # Если нужно перевести месяц на русский
    if is_month_translate:
        month = months_in_russian[date.month - 1]  # Месяцы начинаются с 0 в Python
    else:
        month = str(date.month).zfill(2)  # Месяц с ведущим нулем

    # Форматирование даты
    if is_month_translate:
        formatted_date = f"{day} {month} {year}"
    else:
        formatted_date = f"{day}.{month}.{year}"

    # Если нужно только дату
    return formatted_date

