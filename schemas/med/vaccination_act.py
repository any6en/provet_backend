from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, root_validator
from fastapi import HTTPException

"""Схема записи акта вакцинации, для INSERT(создания)"""
class VaccinationInsertAttributes(BaseModel):
    user_id: int = Field(..., description="Идентификатор врача", gt=0)
    owner_id: int = Field(..., description="Идентификатор владельца", gt=0)
    patient_id: int = Field(..., description="Идентификатор пациента", gt=0)
    vaccine: str = Field(..., min_length=1, max_length=255, description="Название вакцины")
    vaccination_date: datetime = Field(..., description="Дата вакцинации")
    revaccination_date: Optional[datetime] = Field(None, description="Дата ревакцинации (необязательно)")

    @root_validator(pre=True)
    def validate_ids(cls, values):
        keys = values.keys()

        if "user_id" not in keys or not values.get("user_id"):
            raise HTTPException(status_code=400, detail="Не указан идентификатор врача")
        if "owner_id" not in keys or not values.get("owner_id"):
            raise HTTPException(status_code=400, detail="Не указан идентификатор владельца")
        if "patient_id" not in keys or not values.get("patient_id"):
            raise HTTPException(status_code=400, detail="Не указан идентификатор пациента")
        return values

"""Схема записи акта вакцинации, для UPDATE(обновления)"""
class VaccinationUpdateAttributes(BaseModel):
    id: int = Field(..., description="Идентификатор записи вакцинации")

    user_id: Optional[int] = Field(None, description="Идентификатор врача")
    owner_id: Optional[int] = Field(None, description="Идентификатор владельца")
    patient_id: Optional[int] = Field(None, description="Идентификатор пациента")
    vaccine: Optional[str] = Field(None, min_length=1, max_length=255, description="Название вакцины")
    vaccination_date: Optional[datetime] = Field(None, description="Дата вакцинации")
    revaccination_date: Optional[datetime] = Field(None, description="Дата ревакцинации (необязательно)")

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()

        if "id" not in keys or values.get("id") is None:
            raise HTTPException(status_code=400, detail="Не указан идентификатор записи")
        return values

    class Config:
        from_attributes = True
