from decimal import FloatOperation
from tokenize import Double, Floatnumber
from uuid import UUID
from xmlrpc.client import DateTime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Patients(Base):
    __tablename__ = "patients"

    uuid = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String)

class Pharmacies(Base):
    __tablename__ = "pharmacies"

    uuid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)

class Transactions(Base):
    __tablename__ = "transactions"
    
    uuid = Column(Integer, primary_key=True, index=True)
    patient_uuid = Column(String)
    pharmacy_uuid = Column(String)
    amount = Column(String)
    timestamp = Column(String)