from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import logging

from utils.utils import calculate_age


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

# Для отображения таблицы с приемами
async def get_journal_visits(db: AsyncSession, primary_visit_id: int = None):
    query_rows = text("""
        SELECT 
            pv.id AS id, 
            pv.date_visit, 
            pv.user_id, 
            pv.owner_id, 
            pv.patient_id, 
            pv.weight,
            p.animal_type_id as animal_type_id,
            pv.anamnesis,
            pv.examination, 
            pv.prelim_diagnosis,
            pv.confirmed_diagnosis,
            pv.result, 
            pv.disease_onset_date,
            at.name AS animal_name,
            b.name AS breed_name,
            p.nickname AS nickname,
            p.date_birth AS date_birth,
            'Первичный прием' AS content,
            NULL AS primary_visit_id,
            CONCAT(o.first_name, ' ', o.patronymic, ' ', o.last_name) AS owner_full_name
        FROM provet.primary_visits pv
        JOIN provet.patients p ON pv.patient_id = p.id  
        LEFT JOIN provet.animal_types at ON p.animal_type_id = at.id  
        LEFT JOIN provet.breeds b ON p.breed_id = b.id
        JOIN provet.owners o ON pv.owner_id = o.id  -- Объединение с таблицей owners
        WHERE pv.id = :primary_visit_id 

        UNION ALL 

        SELECT 
            rv.id AS id, 
            rv.date_visit,
            rv.user_id, 
            rv.owner_id, 
            rv.patient_id,
            rv.weight, 
            p.animal_type_id as animal_type_id,
            rv.anamnesis,
            rv.examination,
            rv.prelim_diagnosis,
            rv.disease_onset_date,
            rv.confirmed_diagnosis, 
            rv.result, 
            at.name AS animal_name,  
            b.name AS breed_name,     
            p.nickname AS nickname,    
            p.date_birth AS date_birth,
            'Повторный прием' AS content, 
            rv.primary_visit_id AS primary_visit_id,
            CONCAT(o.first_name, ' ', o.patronymic, ' ', o.last_name) AS owner_full_name
        FROM provet.repeat_visits rv
        JOIN provet.patients p ON rv.patient_id = p.id  
        LEFT JOIN provet.animal_types at ON p.animal_type_id = at.id  
        LEFT JOIN provet.breeds b ON p.breed_id = b.id  
        JOIN provet.owners o ON rv.owner_id = o.id  -- Объединение с таблицей owners
        WHERE rv.primary_visit_id = :primary_visit_id 

        ORDER BY date_visit;
    """)

    result_rows = await db.execute(query_rows, {'primary_visit_id': primary_visit_id})
    rows = result_rows.all()

    # Словарь для хранения результатов
    result_map = {}

    for row in rows:
        dict_row = row._asdict()
        logging.error(dict_row)
        logging.error(row)

        # Преобразуем вес в float
        if dict_row.get('weight') is not None:
            dict_row['weight'] = float(dict_row['weight'])

        # Преобразуем дату в ISO формат
        date_visit = dict_row.get('date_visit')
        if date_visit is not None:
            dict_row['date_visit'] = date_visit.isoformat()



        date_birth = dict_row.get('date_birth')
        if date_birth is not None:
            # Вычисление возраста
            age = calculate_age(dict_row['date_visit'], date_birth)
            dict_row['age'] = age
        del dict_row['date_birth']

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
