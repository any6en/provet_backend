from sqlalchemy import Column, Integer, String
from models.model import Base

'''Модель таблицы пользователей в базе данных'''
class UserTable(Base):
    __tablename__ = "users"  # Обратите внимание на двойное подчеркивание

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=False)
    avatar = Column(String(255))
    password = Column(String(255), nullable=False)  # Храните пароли в зашифрованном виде
    role = Column(String(50), nullable=False)

    '''Метод для приведения объекта в словарь'''
    def to_dict(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'patronymic': self.patronymic,
            'avatar': self.avatar if self.avatar else None,
            'role': self.role
        }
