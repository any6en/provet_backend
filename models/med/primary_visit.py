from sqlalchemy import Column, Integer, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.model import Base
from utils.utils import calculate_age


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
    weight = Column(Integer, nullable=True)

    # Опциональные связи (если нужно)
    user = relationship("UserTable")
    owner = relationship("OwnerTable")
    patient = relationship("PatientTable")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'owner_id': self.owner_id,
            'patient_id': self.patient_id,
            'disease_onset_date': self.disease_onset_date,
            'anamnesis': self.anamnesis,
            'examination': self.examination,
            'prelim_diagnosis': self.prelim_diagnosis,
            'confirmed_diagnosis': self.confirmed_diagnosis,
            'result': self.result,
            'date_visit': self.date_visit,
            'weight': float(self.weight) if self.weight else None
        }

    def to_dict_for_document(self):
        return {
            'id': self.id,
            'doctor': self.user.last_name + " " + self.user.first_name[0] + ". " + self.user.patronymic[0] + ".",
            'owner': self.owner.last_name + " " + self.owner.first_name + ". " + self.owner.patronymic,
            'breed': self.patient.breed.name,
            'nickname': self.patient.nickname,
            'age': calculate_age(self.date_visit, self.patient.date_birth),
            'gender': "Самец" if self.patient.gender == 1 else "Самка" if self.patient.gender == 2 else "Не указано",
            'prelim_diagnosis ': self.prelim_diagnosis ,
            'disease_onset_date': self.disease_onset_date,
            'anamnesis': self.anamnesis,
            'examination': self.examination,
            'result': self.result,
            'date_visit': self.date_visit.isoformat() if self.date_visit else None,
            'weight': float(self.weight) if self.weight else None
        }
