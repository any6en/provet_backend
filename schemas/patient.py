from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, Field, root_validator

class PatientInsertAttributes(BaseModel):
    """Атрибуты для вставки животных"""
    nickname: str = Field(..., min_length=1, max_length=255, description="Кличка животного")
    animal_type_id: int = Field(..., description="Идентификатор типа животного")
    breed_id: int = Field(..., description="Идентификатор породы")
    owner_id: int = Field(None, description="Идентификатор владельца")
    date_birth: str = Field(..., description="Дата рождения животного в формате YYYY-MM-DD")
    gender: int = Field(..., description="Пол животного, 0 - мужской, 1 - женский, 2 - неопределённый, 9 - неизвестный")

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()
        if "nickname" not in keys or not values.get("nickname"):
            raise HTTPException(status_code=400, detail="Не указана кличка")
        if "animal_type_id" not in keys or not values.get("animal_type_id"):
            raise HTTPException(status_code=400, detail="Не указан вид животного")
        if "breed_id" not in keys or not values.get("breed_id"):
            raise HTTPException(status_code=400, detail="Не указана порода")
        if "nickname" not in keys or not values.get("nickname"):
            raise HTTPException(status_code=400, detail="Не указана кличка животного")
        if "date_birth" not in keys or not values.get("date_birth"):
            raise HTTPException(status_code=400, detail="Не указана дата рождения животного")
        if "gender" not in keys or values.get("gender") not in [0, 1, 2, 9]:
            raise HTTPException(status_code=400, detail="Неверное значение пола животного")
        return values

class PatientUpdateAttributes(BaseModel):
    """Атрибуты для обновления животных"""
    id: int = Field(..., description="Идентификатор животного")
    nickname: Optional[str] = Field(None, min_length=1, max_length=255, description="Кличка животного")
    animal_type_id: Optional[int] = Field(None, description="Идентификатор типа животного")
    breed_id: Optional[int] = Field(None, description="Идентификатор породы")
    owner_id: Optional[int] = Field(None, description="Идентификатор владельца")
    date_birth: Optional[str] = Field(None, description="Дата рождения животного в формате YYYY-MM-DD")
    gender: Optional[int] = Field(None, description="Пол животного, 0 - мужской, 1 - женский, 2 - неопределённый, 9 - неизвестный")

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()
        if "id" not in keys or not values.get("id"):
            raise HTTPException(status_code=400, detail="Не указан идентификатор животного")
        if "animal_type_id" in keys or values.get("animal_type_id"):
            if "breed_id" not in keys or not values.get("breed_id"):
                raise HTTPException(status_code=400, detail="Не указана порода, но выбран вид")
        return values