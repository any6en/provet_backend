from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import logging


async def get_journal(db: AsyncSession, owner_id: int = None):
    query_rows = text("""
        SELECT 
            primary_visits.id AS id, 
            primary_visits.date_visit AS date, 
            'Первичный прием' AS content,
            users.last_name AS last_name,
            users.first_name AS first_name,
            users.patronymic AS patronymic,
            NULL AS primary_visit_id  
        FROM provet.primary_visits 
        JOIN provet.users ON primary_visits.user_id = users.id
        WHERE primary_visits.owner_id = :owner_id 

        UNION ALL 

        SELECT 
            vaccination_acts.id AS id, 
            vaccination_acts.vaccination_date AS date, 
            'Акт вакцинации' AS content,
            users.last_name AS last_name,
            users.first_name AS first_name,
            users.patronymic AS patronymic,
            NULL AS primary_visit_id  
        FROM provet.vaccination_acts 
        JOIN provet.users ON vaccination_acts.user_id = users.id
        WHERE vaccination_acts.owner_id = :owner_id

        UNION ALL

        SELECT 
            repeat_visits.id AS id, 
            repeat_visits.date_visit AS date, 
            'Повторный прием' AS content, 
            users.last_name AS last_name,
            users.first_name AS first_name,
            users.patronymic AS patronymic,
            repeat_visits.primary_visit_id AS primary_visit_id  
        FROM provet.repeat_visits 
        JOIN provet.users ON repeat_visits.user_id = users.id
        WHERE repeat_visits.owner_id = :owner_id 

        ORDER BY date;
    """)

    result_rows = await db.execute(
        query_rows, {'owner_id': owner_id}
    )
    rows = result_rows.all()

    # Словарь для хранения результатов
    result_map = {}
    primary_visits = []

    for row in rows:
        logging.info(row)
        dict_row = row._asdict()

        # Преобразуем дату в ISO формат
        date = dict_row.get('date')
        if date is not None:
            dict_row['date'] = date.isoformat()

        # Создаем строку с ФИО
        dict_row['doctor'] = f"{dict_row['last_name']} {dict_row['first_name'][0]} {dict_row['patronymic'][0]}."

        if dict_row['primary_visit_id'] is None:
            # Если это первичный прием или акт вакцинации
            result_map[dict_row['id']] = dict_row
            result_map[dict_row['id']]['subRows'] = []
            primary_visits.append(dict_row)
        else:
            # Это повторный прием, добавляем его в subRows соответствующего первичного приема
            if dict_row['primary_visit_id'] in result_map:
                result_map[dict_row['primary_visit_id']]['subRows'].append(dict_row)

    return primary_visits

from datetime import datetime


async def get_journal_visits(db: AsyncSession, primary_visit_id: int = None):
    query_rows = text("""
        SELECT 
            pv.id AS id, 
            pv.date_visit AS date, 
            pv.user_id, 
            pv.owner_id, 
            pv.patient_id, 
            at.name AS animal_name,  
            b.name AS breed_name,     
            p.nickname AS nickname,    
            p.date_birth AS date_birth,
            w.value AS weight,       -- Получаем вес для первичного приема
            'Первичный прием' AS content,
            NULL AS primary_visit_id  
        FROM provet.primary_visits pv
        JOIN provet.patients p ON pv.patient_id = p.id  
        LEFT JOIN provet.animal_types at ON p.animal_type_id = at.id  
        LEFT JOIN provet.breeds b ON p.breed_id = b.id  
        LEFT JOIN provet.weights w ON w.id = pv.weight_id  -- Присоединяем таблицу weights по weight_id
        WHERE pv.id = :primary_visit_id 

        UNION ALL 

        SELECT 
            rv.id AS id, 
            rv.date_visit AS date,
            rv.user_id, 
            rv.owner_id, 
            rv.patient_id,  
            at.name AS animal_name,  
            b.name AS breed_name,     
            p.nickname AS nickname,    
            p.date_birth AS date_birth,
            w.value AS weight,       -- Получаем вес для повторного приема
            'Повторный прием' AS content, 
            rv.primary_visit_id AS primary_visit_id  
        FROM provet.repeat_visits rv
        JOIN provet.patients p ON rv.patient_id = p.id  
        LEFT JOIN provet.animal_types at ON p.animal_type_id = at.id  
        LEFT JOIN provet.breeds b ON p.breed_id = b.id  
        LEFT JOIN provet.weights w ON w.id = rv.weight_id  -- Используем weight_id для повторного приема
        WHERE rv.primary_visit_id = :primary_visit_id 

        ORDER BY date;
    """)

    result_rows = await db.execute(query_rows, {'primary_visit_id': primary_visit_id})
    rows = result_rows.all()

    # Словарь для хранения результатов
    result_map = {}

    for row in rows:
        dict_row = row._asdict()

        # Преобразуем дату в ISO формат
        date = dict_row.get('date')
        if date is not None:
            dict_row['date'] = date.isoformat()

        date_birth = dict_row.get('date_birth')
        if date_birth is not None:
            # Вычисление возраста
            age = calculate_age(dict_row['date'], date_birth)
            dict_row['age'] = age
        del dict_row['date_birth']

        # Преобразуем вес в float
        if dict_row.get('weight') is not None:
            dict_row['weight'] = float(dict_row['weight'])

        if dict_row['primary_visit_id'] is None:
            # Если это первичный прием
            dict_row['subRows'] = []  # Создаем пустой список для подстрок
            result_map[dict_row['id']] = dict_row
        else:
            # Это повторный прием
            if dict_row['primary_visit_id'] in result_map:
                result_map[dict_row['primary_visit_id']]['subRows'].append(dict_row)

    # Предполагается, что только одно первичное посещение возвращается
    primary_visit = result_map.get(primary_visit_id)

    # Возвращаем результат в нужном формате
    return primary_visit if primary_visit else None

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
