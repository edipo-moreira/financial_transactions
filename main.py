from fastapi import Depends, FastAPI
from typing import List
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models, schemas

import utils

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/patients", response_model=List[schemas.Patients])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = utils.get_patients(db, skip=skip, limit=limit)
    return patients

@app.get("/pharmacies", response_model=List[schemas.Patients])
def read_pharmacies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pharmacies = utils.get_pharmacies(db, skip=skip, limit=limit)
    return pharmacies

@app.get("/transactions", response_model=List[schemas.Patients])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = utils.get_transactions(db, skip=skip, limit=limit)
    return transactions