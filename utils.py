from sqlalchemy.orm import Session
import hashlib
import models

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()

def get_pharmacies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pharmacy).offset(skip).limit(limit).all()

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()

def hash_password(password: str):
    return hashlib.md5(password.encode())
