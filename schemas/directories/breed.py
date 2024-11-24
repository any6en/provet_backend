from typing import Optional
from pydantic import BaseModel, Field


"""Схема записи породы животного, для GET(получения)"""
class BreedGetAttributes(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    animal_type_id: int = Field(...)

"""Схема записи породы животного, для INSERT(создания)"""
class BreedInsertAttributes(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    animal_type_id: int = Field(...)


"""Схема записи породы животного, для UPDATE(обновления)"""
class BreedUpdateAttributes(BaseModel):
    id: int = Field(..., description="Идентификатор")
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    animal_type_id: Optional[int] = Field(None)
