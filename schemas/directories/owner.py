from typing import Optional

from fastapi import HTTPException
from pydantic import Field
from datetime import datetime
from pydantic import BaseModel, root_validator

from utils.date_formatter import format_date_dmy_dt

"""Схема записи владельца, для INSERT(создания)"""
class OwnerInsertAttributes(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=255, description="Имя", validate_default=True)
    last_name: str = Field(..., min_length=1, max_length=255, description="Фамилия", validate_default=True)
    patronymic: str = Field(..., min_length=1, max_length=255, description="Отчество", validate_default=True)
    address: Optional[str] = Field(None, min_length=1, max_length=255, description="Адрес проживания")
    date_birth: Optional[datetime] = None
    gender: int = Field(..., ge=0, le=9,
            description="Пол: 0 - неизвестно, 1 - мужской, 2 - женский, 9 - неприменимо", validate_default=True)

    passport_series: str = Field(None, min_length=1, max_length=10, description="Серия паспорта")
    passport_number: str = Field(None, min_length=1, max_length=10, description="Номер паспорта")
    issued_by: str = Field(None, min_length=1, max_length=255, description="Кем выдан")
    subdivision_code: str = Field(None, min_length=1, max_length=10, description="Код подразделения")
    issue_date: str = Field(None, min_length=1, max_length=255, description="Дата выдачи")
    pd_agreement_signed: bool = Field(...,
            description="Подписан ли договор об согласии обработку персональных данных", validate_default=True)
    date_pd_agreement_sign: Optional[datetime] = Field(None,
            description="Дата подписания договора об соглашении на обработку персональных данных")

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()

        if "first_name" not in keys or not values.get("first_name"):
            raise HTTPException(status_code=400, detail="Не указано имя")
        if "last_name" not in keys or not values.get("last_name"):
            raise HTTPException(status_code=400, detail="Не указана фамилия")
        if "patronymic" not in keys or not values.get("patronymic"):
            raise HTTPException(status_code=400, detail="Не указано отчество")
        if "gender" not in keys or not values.get("gender"):
            raise HTTPException( status_code=400, detail="Не указан пол")
        if "pd_agreement_signed" not in keys or values.get("pd_agreement_signed"):
            raise HTTPException(status_code=400, detail="Не указано подписан ли договор СнОПД")
        if "date_pd_agreement_sign" not in keys or values.get("date_pd_agreement_sign"):
            raise HTTPException(status_code=400, detail="Не указана дата подписи договора СнОПД")
        return values

    class Config:
        from_attributes = True

"""Схема записи владельца, для UPDATE(обновления)"""
class OwnerUpdateAttributes(BaseModel):
    id: int = Field(..., description="Идентификатор")

    first_name: Optional[str] = Field(None, min_length=1, max_length=255,
                                      description="Имя", validate_default=True)
    last_name: Optional[str] = Field(None, min_length=1, max_length=255,
                                     description="Фамилия", validate_default=True)
    patronymic: Optional[str] = Field(None, min_length=1, max_length=255,
                                      description="Отчество", validate_default=True)
    address: Optional[str] = Field(None, max_length=255,
                                   description="Адрес", validate_default=True)
    date_birth: Optional[datetime] = Field(None,
                                           description="Дата рождения", validate_default=True)
    gender: Optional[int] = Field(None, ge=0, le=9,
            description="Пол: 0 - неизвестно, 1 - мужской, 2 - женский, 9 - неприменимо")

    passport_series: Optional[str] = Field(None, min_length=1, max_length=10, description="Серия паспорта")
    passport_number: Optional[str] = Field(None, min_length=1, max_length=10, description="Номер паспорта")
    issued_by: Optional[str] = Field(None, min_length=1, max_length=255, description="Кем выдан паспорт")
    subdivision_code: Optional[str] = Field(None, min_length=1, max_length=10,
                                            description="Код подразделения выдачи паспорта")
    issue_date: Optional[datetime] = Field(None, description="Дата рождения")
    pd_agreement_signed: bool = Field(...,
        description="Подписан ли договор об согласии на обработку персональных данных", validate_default=True)
    date_pd_agreement_sign: Optional[datetime] = Field(None,
        description="Дата подписания договора об соглашении на обработку персональных данных")

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()

        if "id" not in keys or not values.get("id"):
            raise HTTPException(status_code=400, detail="Не указан идентификатор")
        return values

"""Схема записи владельца договора об согласии на обработку персональных данных"""
class OwnerAgreementSignPD(BaseModel):  # Inherit from BaseModel
    first_name: str = Field(..., min_length=1, max_length=255, description="Имя")
    last_name: str = Field(..., min_length=1, max_length=255, description="Фамилия")
    patronymic: str = Field(..., min_length=1, max_length=255, description="Отчество")
    address: Optional[str] = Field(..., max_length=255, description="Адрес")

    passport_series: str = Field(..., min_length=1, max_length=10, description="Серия паспорта")
    passport_number: str = Field(..., min_length=1, max_length=10, description="Номер паспорта")
    issued_by: str = Field(..., min_length=1, max_length=255, description="Кем выдан паспорт")
    subdivision_code: str = Field(..., min_length=1, max_length=10,
            description="Код подразделения выдачи паспорта")
    issue_date: Optional[datetime] = Field(..., description="Дата выдачи паспорта")

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()

        if "first_name" not in keys or not values.get("first_name"):
            raise HTTPException(status_code=400, detail="Не указано имя")
        if "last_name" not in keys or not values.get("last_name"):
            raise HTTPException(status_code=400, detail="Не указана фамилия")
        if "patronymic" not in keys or not values.get("patronymic"):
            raise HTTPException(status_code=400, detail="Не указано отчество")
        if "address" not in keys or not values.get("address"):
            raise HTTPException(status_code=400, detail="Не указан адрес")
        if "passport_series" not in keys or not values.get("passport_series"):
            raise HTTPException(status_code=400, detail="Не указана серия паспорта")
        if "passport_number" not in keys or not values.get("passport_number"):
            raise HTTPException(status_code=400, detail="Не указан номер паспорта")
        if "issued_by" not in keys or not values.get("issued_by"):
            raise HTTPException(status_code=400, detail="Не указан кем выдан паспорт")
        if "subdivision_code" not in keys or not values.get("subdivision_code"):
            raise HTTPException(status_code=400, detail="Не указан код подразделения выдачи паспорта")
        if "issue_date" not in keys or not values.get("issue_date"):
            raise HTTPException(status_code=400, detail="Не указана дата выдачи паспорта")
        return values

    # Преобразование схемы в словарь
    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'patronymic': self.patronymic,
            'address': self.address,

            'passport_series': self.passport_series,
            'passport_number': self.passport_number,
            'issued_by': self.issued_by,
            'subdivision_code': self.subdivision_code,
            'issue_date': self.issue_date.isoformat(),
            'date_sign': format_date_dmy_dt(datetime.now().isoformat(), False, True)
        }
