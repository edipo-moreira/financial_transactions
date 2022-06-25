from sqlalchemy.orm import Session

import models

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patients).offset(skip).limit(limit).all()

def get_pharmacies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pharmacies).offset(skip).limit(limit).all()

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transactions).offset(skip).limit(limit).all()