from sqlalchemy import Column, Integer, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.model import Base


class PrimaryVisit(Base):
    __tablename__ = "primary_visits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Ссылка на врача
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)  # Ссылка на владельца
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)  # Ссылка на пациента
    disease_onset_date = Column(Date, nullable=False)  # Дата возникновения болезни
    anamnesis = Column(Text, nullable=False)  # Анамнез
    examination = Column(Text, nullable=False)  # Обследование
    prelim_diagnosis = Column(Text, nullable=False)  # Предварительный диагноз
    confirmed_diagnosis = Column(Text, nullable=False)  # Подтвержденный диагноз
    result = Column(Text, nullable=False)  # Результат
    date_visit = Column(DateTime, nullable=False)  # Дата посещения

    # Опциональные связи (если нужно)
    user = relationship("UserTable")  # Предполагая, что у вас есть модель User
    owner = relationship("OwnerTable")  # Предполагая, что у вас есть модель Owner
    patient = relationship("PatientTable")  # Предполагая, что у вас есть модель Patient
