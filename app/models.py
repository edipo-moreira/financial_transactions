from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "user"

    uuid = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)


class UserInDB(User):
    password: str


class Patient(Base):
    __tablename__ = "patient"

    uuid = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String)

    patient = relationship("Transaction", back_populates="patient")


class Pharmacy(Base):
    __tablename__ = "pharmacy"

    uuid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)

    pharmacy = relationship("Transaction", back_populates="pharmacy")


class Transaction(Base):
    __tablename__ = "transaction"

    uuid = Column(Integer, primary_key=True, index=True)
    patient_uuid = Column(Integer, ForeignKey("patient.uuid"))
    pharmacy_uuid = Column(Integer, ForeignKey("pharmacy.uuid"))
    amount = Column(String)
    timestamp = Column(String)

    patient = relationship("Patient", back_populates="patient")
    pharmacy = relationship("Pharmacy", back_populates="pharmacy")
