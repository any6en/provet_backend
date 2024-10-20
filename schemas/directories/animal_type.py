from fastapi import HTTPException
from pydantic import Field
from pydantic import BaseModel, root_validator

class AnimalTypeGetAttributes(BaseModel):
    """Атрибуты типов животных"""
    id: int = Field(...)
    name: str = Field(...)

class AnimalTypeInsertAttributes(BaseModel):
    """Атрибуты типов животных"""
    name: str = Field(..., min_length=1, max_length=255, description="Имя, от 1 до 255 символов", validate_default=True)

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()
        if "name" not in keys or not values.get("name"):
            raise HTTPException(
                status_code=400,
                detail="Не указано название"
            )
        return values

class AnimalTypeUpdateAttributes(BaseModel):
    """Атрибуты владельцев"""
    id: int = Field(..., description="Идентификатор")

    name: str = Field(..., min_length=1, max_length=255, description="Имя, от 1 до 255 символов", validate_default=True)

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()
        if "name" not in keys or not values.get("name"):
            raise HTTPException(
                status_code=400,
                detail="Не указано название"
            )
        return values