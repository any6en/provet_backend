from typing import Optional
from pydantic import BaseModel, Field

"""Схема записи пациента, для INSERT(создания)"""
class PatientInsertAttributes(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=25)

    animal_type_id: int = Field(...)
    breed_id: int = Field(...)
    owner_id: int = Field(None)

    color: str = Field(None, min_length=1, max_length=50)
    is_castrated: bool = Field(...)

    date_birth: str = Field(...)
    gender: int = Field(..., ge=0, le=9)


"""Схема записи пациента, для UPDATE(обновления)"""
class PatientUpdateAttributes(BaseModel):
    nickname: Optional[str] = Field(None, min_length=1, max_length=25)

    id: int = Field(...)
    animal_type_id: Optional[int] = Field(None)
    breed_id: Optional[int] = Field(None)
    owner_id: Optional[int] = Field(None)

    color: Optional[str] = Field(None, min_length=1, max_length=50)
    is_castrated: Optional[bool] = Field(None)

    date_birth: Optional[str] = Field(None)
    gender: Optional[int] = Field(None, ge=0, le=9)
