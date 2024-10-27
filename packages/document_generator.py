
from docxtpl import DocxTemplate
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from sqlalchemy.orm import selectinload
from starlette.responses import FileResponse
from sqlalchemy import text, select

from models.directories.owner import OwnerTable
from models.directories.patient import PatientTable
from models.med.primary_visit import PrimaryVisitTable
from utils.utils import calculate_age


async def get_document_primary_visit(db: AsyncSession, primary_visit_id: int):
    query = await db.execute(
        select(PrimaryVisitTable)
        .options(
            selectinload(PrimaryVisitTable.user),
            selectinload(PrimaryVisitTable.owner),
            selectinload(PrimaryVisitTable.patient).selectinload(PatientTable.breed)  # Загрузка породы
        )
        .filter_by(id=primary_visit_id)
    )

    primary_visit = query.scalars().first()

    if primary_visit is None:
        return None

    primary_visit = primary_visit.to_dict_for_document()
    logging.error(primary_visit)
    logging.info(primary_visit)

    doc = DocxTemplate("resources/Назначение.docx")
    doc.render(primary_visit)

    doc.save(f"resources/{primary_visit['nickname']}{primary_visit['id']}_первичный_прием.docx")

    return FileResponse(
        path=f"resources/{primary_visit['nickname']}{primary_visit['id']}_первичный_прием.docx",
        filename=f"{primary_visit['nickname']}{primary_visit['id']}_первичный_прием.docx",
        media_type='multipart/form-data'
    )


# row = query.scalars().first()
#     row = row.to_dict_for_document()
#
#     doc = DocxTemplate("resources/СНоПД.docx")
#
#     doc.render(row)
#     doc.save("resources/шаблон-final123.docx")
#
#     return FileResponse(path='resources/шаблон-final123.docx', filename='Говно228.docx', media_type='multipart/form-data')


async def get_consent_processing_personal_data(db: AsyncSession, owner_id: int = None):
    if owner_id is not None:
        # Если owner_id найден, получаем информацию о владельце
        query = await (
            db.execute(
                select(OwnerTable)
                .filter_by(id=owner_id)
            )
        )
        owner_document = query.scalars().first().to_dict_for_document()

    doc = DocxTemplate("resources/СНоПД.docx")
    doc.render(owner_document)

    doc.save("resources/" + owner_document["owner"] + "_согласие.docx")

    return FileResponse(path="resources/" + owner_document["owner"] + "_согласие.docx", filename=owner_document["owner"] + "_согласие.docx",
                        media_type='multipart/form-data')
