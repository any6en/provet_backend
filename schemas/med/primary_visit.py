from decimal import Decimal
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, root_validator
from fastapi import HTTPException

"""Схема записи первичного приема, для INSERT(создания)"""
class PrimaryVisitInsertAttributes(BaseModel):
    user_id: int = Field(...)
    owner_id: int = Field(...)
    patient_id: int = Field(...)
    disease_onset_date: datetime = Field(...)
    anamnesis: str = Field(...)
    examination: str = Field(...)
    prelim_diagnosis: str = Field(...)
    confirmed_diagnosis: str = Field(None)
    result: str = Field(...)
    date_visit: Optional[datetime] = Field(default_factory=datetime.now)
    weight: Optional[Decimal] = Field(None)

    @root_validator(pre=True)
    def validate_ids(cls, values):
        keys = values.keys()

        weight = values.get("weight")
        if weight is not None:
            if not isinstance(weight, (int, float)):
                try:
                    values["weight"] = float(weight)  # Пытаемся конвертировать в float
                except (ValueError, TypeError):
                    raise HTTPException(status_code=400, detail="Вес должен быть числом")
        if "user_id" not in keys or values.get("user_id") is None:
            raise HTTPException(status_code=400, detail="Не указан идентификатор врача")
        if "owner_id" not in keys or values.get("owner_id") is None:
            raise HTTPException(status_code=400, detail="Не указан идентификатор владельца")
        if "patient_id" not in keys or values.get("patient_id") is None:
            raise HTTPException(status_code=400, detail="Не указан идентификатор пациента")
        if "disease_onset_date" not in keys or values.get("disease_onset_date") is None:
            raise HTTPException(status_code=400, detail="Не указана дата возникновения болезни")
        if "anamnesis" not in keys or not values.get("anamnesis"):
            raise HTTPException(status_code=400, detail="Не указан анамнез")
        if "examination" not in keys or not values.get("examination"):
            raise HTTPException(status_code=400, detail="Не указано обследование")
        if "prelim_diagnosis" not in keys or not values.get("prelim_diagnosis"):
            raise HTTPException(status_code=400, detail="Не указан предварительный диагноз")
        if "confirmed_diagnosis" not in keys or not values.get("confirmed_diagnosis"):
            raise HTTPException(status_code=400, detail="Не указан подтвержденный диагноз")
        if "result" not in keys or not values.get("result"):
            raise HTTPException(status_code=400, detail="Не указан результат")

        return values

"""Схема записи первичного приема, для UPDATE(обновления)"""
class PrimaryVisitUpdateAttributes(BaseModel):
    id: int = Field(..., description="Идентификатор записи о посещении")

    user_id: Optional[int] = Field(None, description="Идентификатор врача")

    owner_id: Optional[int] = Field(None, description="Идентификатор владельца")
    patient_id: Optional[int] = Field(None, description="Идентификатор пациента")
    disease_onset_date: Optional[datetime] = Field(None, description="Дата возникновения болезни")
    anamnesis: Optional[str] = Field(None, description="Анамнез")
    examination: Optional[str] = Field(None, description="Обследование")
    prelim_diagnosis: Optional[str] = Field(None, description="Предварительный диагноз")
    confirmed_diagnosis: Optional[str] = Field(None, description="Подтвержденный диагноз")
    result: Optional[str] = Field(None, description="Результат")
    date_visit: Optional[datetime] = Field(None, description="Дата посещения (по умолчанию текущее время)")
    weight: Optional[Decimal] = Field(None, description="вес (тип DECIMAL(10, 2))")

    class Config:
        from_attributes = True
