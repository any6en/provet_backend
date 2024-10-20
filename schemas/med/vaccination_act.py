from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, root_validator
from fastapi import HTTPException


class VaccinationInsertAttributes(BaseModel):
    """Атрибуты вакцинации"""
    user_id: int = Field(..., description="Идентификатор врача", gt=0)
    owner_id: int = Field(..., description="Идентификатор владельца", gt=0)
    patient_id: int = Field(..., description="Идентификатор пациента", gt=0)
    vaccine: str = Field(..., min_length=1, max_length=255, description="Название вакцины")
    vaccination_date: datetime = Field(..., description="Дата вакцинации")
    revaccination_date: Optional[datetime] = Field(None, description="Дата ревакцинации (необязательно)")

    @root_validator(pre=True)
    def validate_ids(cls, values):
        user_id = values.get("user_id")
        owner_id = values.get("owner_id")
        patient_id = values.get("patient_id")

        if user_id is None:
            raise HTTPException(status_code=400, detail="Не указан идентификатор врача")
        if owner_id is None:
            raise HTTPException(status_code=400, detail="Не указан идентификатор владельца")
        if patient_id is None:
            raise HTTPException(status_code=400, detail="Не указан идентификатор пациента")

        return values


class VaccinationUpdateAttributes(BaseModel):
    """Атрибуты вакцинации для обновления"""
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

        # Проверяем, что хотя бы одно поле для обновления указано
        if all(key not in keys for key in
               ["user_id", "owner_id", "patient_id", "vaccine", "vaccination_date", "revaccination_date"]):
            raise HTTPException(
                status_code=400,
                detail="Не указаны данные для обновления"
            )

        # Проверяем, что все обязательные поля для обновления указаны
        if "vaccination_date" not in keys or not values.get("vaccination_date"):
            raise HTTPException(
                status_code=400,
                detail="Дата вакцинации должна быть указана, если обновляется"
            )

        return values

    class Config:
        from_attributes = True
