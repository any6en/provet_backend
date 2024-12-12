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

    disease_onset_date: datetime = Field(None)
    anamnesis: str = Field(...)
    examination: str = Field(...)
    prelim_diagnosis: str = Field(None)
    confirmed_diagnosis: str = Field(None)
    result: str = Field(...)
    date_visit: Optional[datetime] = Field(default_factory=datetime.now)
    weight: Optional[Decimal] = Field(None)

"""Схема записи первичного приема, для UPDATE(обновления)"""
class PrimaryVisitUpdateAttributes(BaseModel):
    id: int = Field(...)

    user_id: Optional[int] = Field(None)
    owner_id: Optional[int] = Field(None)
    patient_id: Optional[int] = Field(None)

    disease_onset_date: Optional[datetime] = Field(None)
    anamnesis: Optional[str] = Field(None)
    examination: Optional[str] = Field(None)
    prelim_diagnosis: Optional[str] = Field(None)
    confirmed_diagnosis: Optional[str] = Field(None)
    result: Optional[str] = Field(None)
    date_visit: Optional[datetime] = Field(None)
    weight: Optional[Decimal] = Field(None)

    class Config:
        from_attributes = True
