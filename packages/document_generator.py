from docxtpl import DocxTemplate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.responses import FileResponse
from sqlalchemy import select
from docx2pdf import convert  # Импортируем библиотеку для конвертации

# Другие необходимые импорты
from models.directories.owner import OwnerTable
from models.directories.patient import PatientTable
from models.med.primary_visit import PrimaryVisitTable
from models.med.repeat_visit import RepeatVisitTable
from schemas.directories.owner import OwnerAgreementSignPD

from utils.responses import Http400, create_http_response


async def get_document_primary_visit(db: AsyncSession, primary_visit_id: int):
    query = await db.execute(
        select(PrimaryVisitTable)
        .options(
            selectinload(PrimaryVisitTable.user),
            selectinload(PrimaryVisitTable.owner),
            selectinload(PrimaryVisitTable.patient).selectinload(PatientTable.breed),
            selectinload(PrimaryVisitTable.patient).selectinload(PatientTable.animal_type)
        )
        .filter_by(id=primary_visit_id)
    )

    primary_visit = query.scalars().first()

    if primary_visit is None:
        return None

    primary_visit = primary_visit.to_dict_for_document()

    docx_path = f"resources/{primary_visit['nickname']}{primary_visit['id']}_первичный_прием.docx"
    pdf_path = f"resources/{primary_visit['nickname']}{primary_visit['id']}_первичный_прием.pdf"

    doc = DocxTemplate("resources/Назначение.docx")
    doc.render(primary_visit)
    doc.save(docx_path)

    # Конвертация в PDF
    convert(docx_path, pdf_path)

    return FileResponse(
        path=pdf_path,
        filename=f"{primary_visit['nickname']}{primary_visit['id']}_первичный_прием.pdf",
        media_type='application/pdf'  # Измените на pdf
    )

async def get_document_repeat_visit(db: AsyncSession, repeat_visit_id: int):
    query = await db.execute(
        select(RepeatVisitTable)
        .options(
            selectinload(RepeatVisitTable.user),
            selectinload(RepeatVisitTable.owner),
            selectinload(RepeatVisitTable.patient).selectinload(PatientTable.breed),
            selectinload(RepeatVisitTable.patient).selectinload(PatientTable.animal_type)
    )
        .filter_by(id=repeat_visit_id)
    )

    repeat_visit = query.scalars().first()

    if repeat_visit is None:
        return create_http_response(Http400("Такой записи не существует"))

    repeat_visit = repeat_visit.to_dict_for_document()

    docx_path = f"resources/{repeat_visit['nickname']}{repeat_visit['id']}_повторный_прием.docx"
    pdf_path = f"resources/{repeat_visit['nickname']}{repeat_visit['id']}_повторный_прием.pdf"

    doc = DocxTemplate("resources/Назначение.docx")
    doc.render(repeat_visit)
    doc.save(docx_path)

    # Конвертация в PDF
    convert(docx_path, pdf_path)

    return FileResponse(
        path=pdf_path,
        filename=f"{repeat_visit['nickname']}{repeat_visit['id']}_повторный_прием.pdf",
        media_type='application/pdf'  # Измените на pdf
    )

async def get_pd_agreement_sign(db: AsyncSession, record: OwnerAgreementSignPD):
    record = record.to_dict()
    docx_path = f"resources/{ record['last_name'] + record['first_name'] + record['patronymic'] }_согласие.docx"
    pdf_path = f"resources/{ record['last_name'] + record['first_name'] + record['patronymic']}_согласие.pdf"

    doc = DocxTemplate("resources/СНоПД.docx")
    doc.render(record)
    doc.save(docx_path)

    # Конвертация в PDF
    convert(docx_path, pdf_path)

    return FileResponse(
        path=pdf_path,
        filename=record['last_name'] + record['first_name'] + record['patronymic'] + "_согласие.pdf",
        media_type='application/pdf'
    )
