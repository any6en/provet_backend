from sqlalchemy import Column, Integer, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.model import Base

class PrimaryVisitTable(Base):
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
    # user = relationship("UserTable")
    # owner = relationship("OwnerTable")
    # patient = relationship("PatientTable")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'owner_id': self.owner_id,
            'patient_id': self.patient_id,
            'disease_onset_date': self.disease_onset_date.isoformat() if self.disease_onset_date else None,
            'anamnesis': self.anamnesis,
            'examination': self.examination,
            'prelim_diagnosis': self.prelim_diagnosis,
            'confirmed_diagnosis': self.confirmed_diagnosis,
            'result': self.result,
            'date_visit': self.date_visit.isoformat() if self.date_visit else None
        }
