from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import logging

from models.med.primary_visits import PrimaryVisit
from models.med.vaccination_act import VaccinationAct
from models.user import UserTable


async def get_journal(db: AsyncSession, id: int = None):
    # Запрос объединяет вакцины и первичные визиты и сортирует по дате
    query = await db.execute(
        select(VaccinationAct, PrimaryVisit)
        .options(selectinload(VaccinationAct.user))
        .options(selectinload(PrimaryVisit.user))
        .outerjoin(PrimaryVisit, VaccinationAct.patient_id == VaccinationAct.patient_id)
        .order_by(VaccinationAct.vaccination_date.desc())  # Сортируем по дате вакцинации в порядке убывания
    )
    logging.error(str(
        select(VaccinationAct, PrimaryVisit).filter_by(VaccinationAct.patient_id == id).filter_by(PrimaryVisit.patient_id == id)));
    results = query.all()
    result = []

    # Формируем результат из обеих таблиц
    for vaccination_act, primary_visit in results:
        # Добавляем данные о вакцинации
        if vaccination_act:
            result.append({
                "id": vaccination_act.id,
                "date": vaccination_act.vaccination_date.isoformat(),  # Предполагаем, что есть поле date в VaccinationAct
                "year": vaccination_act.vaccination_date.isoformat() if vaccination_act.vaccination_date else None,
                "content": "Акт вакцинации",
                "doctor": vaccination_act.user.first_name  # Или аналогичное поле
            })

        # Если также нужно добавить данные из PrimaryVisit
        if primary_visit:
            result.append({
                "id": primary_visit.id,
                "date": primary_visit.date_visit.isoformat(),  # Предполагаем, что есть поле date_visit в PrimaryVisit
                "year": primary_visit.date_visit.isoformat() if primary_visit.date_visit else None,
                "content": "Первичный прием",
                "doctor": primary_visit.user.first_name  # Или аналогичное поле
            })

    return result
