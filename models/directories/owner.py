from sqlalchemy import Column, Integer, String, Date, DateTime
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
    date_birth = Column(Date)
    gender = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    # Поспортные данные
    passport_series = Column(String(255), nullable=True)
    passport_number = Column(String(255), nullable=True)
    issued_by = Column(String(255), nullable=True)
    subdivision_code = Column(String(255), nullable=True)
    issue_date = Column(Date)
    pd_agreement_signed = Column(String(255), nullable=False)
    date_pd_agreement_sign = Column(Date, nullable=False)

    '''Метод для приведения объекта в словарь'''
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'patronymic': self.patronymic,
            'address': self.address if self.address else None,
            'date_birth': self.date_birth.isoformat() if self.date_birth else None,
            'gender': self.gender,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'passport_series': self.passport_series if self.passport_series else None,
            'passport_number': self.passport_number if self.passport_number else None,
            'issued_by': self.issued_by if self.issued_by else None,
            'subdivision_code': self.subdivision_code if self.subdivision_code else None,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'pd_agreement_signed': self.pd_agreement_signed if self.pd_agreement_signed else None,
            'date_pd_agreement_sign': self.pd_agreement_signed if self.pd_agreement_signed else None
        }