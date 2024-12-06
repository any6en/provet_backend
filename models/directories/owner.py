from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from models.model import Base

'''Модель таблицы владельцов в базе данных'''
class OwnerTable(Base):
    __tablename__ = "owners"
    # Основные данные
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    patronymic = Column(String(255), nullable=False)
    address = Column(String(255))
    phone_number = Column(String)
    date_birth = Column(Date)
    gender = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    # Поспортные данные
    passport_series = Column(String(255), nullable=True)
    passport_number = Column(String(255), nullable=True)
    passport_issued_by = Column(String(255), nullable=True)
    passport_subdivision_code = Column(String(255), nullable=True)
    passport_issue_date = Column(Date, nullable=True)
    pd_agreement_signed = Column(Boolean, nullable=False)
    date_pd_agreement_sign = Column(Date, nullable=True)

    '''Метод для приведения объекта в словарь'''
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'patronymic': self.patronymic,
            'address': self.address,
            'phone_number': self.phone_number if self.phone_number else None,
            'date_birth': self.date_birth.isoformat() if self.date_birth else None,
            'gender': self.gender,
            'created_at': self.created_at.isoformat(),
            'passport_series': self.passport_series,
            'passport_number': self.passport_number,
            'passport_issued_by': self.passport_issued_by,
            'passport_subdivision_code': self.passport_subdivision_code ,
            'passport_issue_date': self.passport_issue_date.isoformat() if self.passport_issue_date else None,
            'pd_agreement_signed': self.pd_agreement_signed,
            'date_pd_agreement_sign': self.date_pd_agreement_sign.isoformat()
                if self.date_pd_agreement_sign else None
        }