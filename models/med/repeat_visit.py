from sqlalchemy import Column, Integer, Date, DateTime, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from models.model import Base

class RepeatVisitTable(Base):
    __tablename__ = "repeat_visits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Ссылка на врача
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)  # Ссылка на владельца
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)  # Ссылка на пациента
    primary_visit_id = Column(Integer, ForeignKey('primary_visits.id'), nullable=False)  # Ссылка на первичное посещение
    disease_onset_date = Column(Date, nullable=False)  # Дата возникновения болезни
    anamnesis = Column(Text, nullable=False)  # Анамнез
    examination = Column(Text, nullable=False)  # Обследование
    prelim_diagnosis = Column(Text, nullable=False)  # Предварительный диагноз
    confirmed_diagnosis = Column(Text, nullable=False)  # Подтвержденный диагноз
    result = Column(Text, nullable=False)  # Результат
    date_visit = Column(DateTime, nullable=False)  # Дата посещения
    weight = Column(Integer, nullable=True)

    # Опциональные связи
    user = relationship("UserTable")  # Связь с врачом
    owner = relationship("OwnerTable")  # Связь с владельцем
    patient = relationship("PatientTable")  # Связь с пациентом
    primary_visit = relationship("PrimaryVisit")  # Связь с первичным посещением
