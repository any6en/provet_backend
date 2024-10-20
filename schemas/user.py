from pydantic import BaseModel

class User(BaseModel):
    id: int
    login: str
    email: str
    first_name: str
    last_name: str
    patronymic: str
    avatar: str
    password: str
    role: str
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    login: str
    password: str
