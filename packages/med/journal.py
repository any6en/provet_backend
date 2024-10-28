from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
import logging

from sqlalchemy.orm import selectinload

from models.directories.patient import PatientTable
from models.med.primary_visit import PrimaryVisitTable
from models.med.repeat_visit import RepeatVisitTable
from models.med.vaccination_act import VaccinationActTable


# Для отображения таблицы с приемами
async def get_journal(db: AsyncSession, patient_id: int = None):
    # Запрашиваем первичные визиты
    query = await db.execute(
        select(PrimaryVisitTable)
        .options(
            selectinload(PrimaryVisitTable.user),
            selectinload(PrimaryVisitTable.owner),
            selectinload(PrimaryVisitTable.patient).selectinload(PatientTable.breed),
            selectinload(PrimaryVisitTable.patient).selectinload(PatientTable.animal_type)
        )
        .filter(PrimaryVisitTable.patient_id == patient_id)
    )

    # Первичные приемы
    primary_visits = query.scalars().all()
    primary_visits_list = [pv.to_dict_journal() for pv in primary_visits]
    logging.error(primary_visits)

    # Запрашиваем повторные визиты
    repeat_query = await db.execute(
        select(RepeatVisitTable)
        .options(
            selectinload(RepeatVisitTable.user),
            selectinload(RepeatVisitTable.owner),
            selectinload(RepeatVisitTable.patient).selectinload(PatientTable.breed),
            selectinload(RepeatVisitTable.patient).selectinload(PatientTable.animal_type)
        )
        .filter(RepeatVisitTable.patient_id == patient_id)
    )

    # Повторные приемы
    repeat_visits = repeat_query.scalars().all()
    repeat_visits_list = [rv.to_dict_journal() for rv in repeat_visits]
    logging.error(repeat_visits_list)

    # Запрашиваем акты вакцинации
    vac_act_query = await db.execute(
        select(VaccinationActTable)
        .options(
            selectinload(VaccinationActTable.user),
            selectinload(VaccinationActTable.owner),
            selectinload(VaccinationActTable.patient).selectinload(PatientTable.breed),
            selectinload(VaccinationActTable.patient).selectinload(PatientTable.animal_type)
        )
        .filter(VaccinationActTable.patient_id == patient_id)
    )

    # Акты вакцинации
    vac_acts = vac_act_query.scalars().all()
    vac_acts_list = [va.to_dict_journal() for va in vac_acts]
    logging.error(vac_acts_list)

    # Структура ответа
    response_data = []

    # Объединяем первичные визиты и соответствующие повторные визиты
    for pv in primary_visits_list:
        # Добавляем все повторные приемы, соответствующие этому первичному визиту
        for rv in repeat_visits_list:
            if rv['primary_visit_id'] == pv['id']:
                pv['subRows'].append(rv)

        # Добавляем первичный визит в результирующий список
        response_data.append(pv)

    # Теперь добавим акты вакцинации
    for va in vac_acts_list:
        response_data.append(va)

    return response_data

async def get_journal_visits(db: AsyncSession, primary_visit_id: int = None):
    # Запрашиваем первичный визит
    query = await db.execute(
        select(PrimaryVisitTable)
        .options(
            selectinload(PrimaryVisitTable.user),
            selectinload(PrimaryVisitTable.owner),
            selectinload(PrimaryVisitTable.patient).selectinload(PatientTable.breed),
            selectinload(PrimaryVisitTable.patient).selectinload(PatientTable.animal_type)
        )
        .filter(PrimaryVisitTable.id == primary_visit_id)
    )

    primary_visit = query.scalars().first()
    logging.info(primary_visit)
    logging.error(primary_visit)
    if primary_visit is None:
        return None

    # Получение данных первичного визита
    primary_visit_dict = primary_visit.to_dict_visits()

    # Запрашиваем повторные визиты
    repeat_query = await db.execute(
        select(RepeatVisitTable)
        .options(
            selectinload(RepeatVisitTable.user),
            selectinload(RepeatVisitTable.owner),
            selectinload(RepeatVisitTable.patient).selectinload(PatientTable.breed),
            selectinload(RepeatVisitTable.patient).selectinload(PatientTable.animal_type)
        )
        .filter(RepeatVisitTable.primary_visit_id == primary_visit_id)
    )

    repeat_visits = repeat_query.scalars().all()
    repeat_visits_list = [rv.to_dict_visits() for rv in repeat_visits]

    # Объединяем данные
    primary_visit_dict['subRows'] = repeat_visits_list
    return primary_visit_dict

    # Возвращаем результат в нужном формате
    return primary_visit if primary_visit else None
