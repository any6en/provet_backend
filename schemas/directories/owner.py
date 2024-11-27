from typing import Optional

from pydantic import Field
from datetime import datetime
from pydantic import BaseModel

from utils.date_formatter import format_date_dmy_dt

"""Схема записи владельца, для INSERT(создания)"""
class OwnerInsertAttributes(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=25)
    last_name: str = Field(..., min_length=1, max_length=50)
    patronymic: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(None, min_length=10, max_length=11)
    address: Optional[str] = Field(None, min_length=1, max_length=255)
    date_birth: Optional[datetime] = Field(None)
    gender: int = Field(..., ge=0, le=9)

    passport_series: int = Field(None, ge=1000, le=9999)
    passport_number: int = Field(None, ge=100000, le=999999)
    passport_issued_by: str = Field(None, min_length=1, max_length=255)
    passport_subdivision_code: int = Field(None, ge=100000, le=999999)
    passport_issue_date: Optional[datetime] = Field(None)
    pd_agreement_signed: bool = Field(..., description="Подписан СНоПД")
    date_pd_agreement_sign: Optional[datetime] = Field(None, description="Дата подписания СНоПД")


    class Config:
        from_attributes = True

"""Схема записи владельца, для UPDATE(обновления)"""
class OwnerUpdateAttributes(BaseModel):
    id: int = Field(..., description="Идентификатор")

    first_name: Optional[str] = Field(None, min_length=1, max_length=25)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    patronymic: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: str = Field(None, min_length=10, max_length=11)
    address: Optional[str] = Field(None, min_length=1, max_length=255)
    date_birth: Optional[datetime] = Field(None)
    gender: Optional[int] = Field(None, ge=0, le=9)

    passport_series: Optional[int] = Field(None, ge=1000, le=9999)
    passport_number: Optional[int] = Field(None, ge=100000, le=999999)
    passport_issued_by: Optional[str] = Field(None, min_length=1, max_length=255)
    passport_subdivision_code: Optional[int] = Field(None, ge=100000, le=999999)
    passport_issue_date: Optional[datetime] = Field(None)

    pd_agreement_signed: bool = Field(None, description="Подписано ли СНоПД")
    date_pd_agreement_sign: Optional[datetime] = Field(None, description="Дата подписания СНоПД")

"""Схема записи владельца договора об согласии на обработку персональных данных"""
class OwnerAgreementSignPD(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=25)
    last_name: str = Field(..., min_length=1, max_length=50)
    patronymic: str = Field(..., min_length=1, max_length=50)
    address: Optional[str] = Field(..., max_length=255)

    passport_series: int = Field(..., ge=1000, le=9999)
    passport_number: int = Field(..., ge=100000, le=999999)
    passport_issued_by: str = Field(..., min_length=1, max_length=255)
    passport_subdivision_code: int = Field(..., ge=100000, le=999999)
    passport_issue_date: Optional[datetime] = Field(...)

    # Преобразование схемы в словарь
    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'patronymic': self.patronymic,
            'address': self.address,

            'passport_series': self.passport_series,
            'passport_number': self.passport_number,
            'passport_issued_by': self.passport_issued_by,
            'passport_subdivision_code': self.passport_subdivision_code,
            'passport_issue_date': format_date_dmy_dt(self.passport_issue_date.isoformat(), False, True),
            'date_sign': format_date_dmy_dt(datetime.now().isoformat(), False, True)
        }
