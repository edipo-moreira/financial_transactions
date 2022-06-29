import app.schemas as schemas
import app.utils as utils

from fastapi import Depends, FastAPI, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta
from typing import List
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.models import User
from decouple import config

app = FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: dict = Body(...), db: Session = Depends(get_db)):
    user = utils.authenticate_user(db, form_data.get('username'), form_data.get('password'))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: User = Depends(utils.get_current_user)):
	users = utils.get_users(db, skip=skip, limit=limit)
	return users

@app.post("/user/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), _: User = Depends(utils.get_current_user)):
    db_user = utils.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return utils.create_user(db=db, user=user)

@app.get("/patients", response_model=List[schemas.Patient])
async def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: User = Depends(utils.get_current_user)):
	patients = utils.get_patients(db, skip=skip, limit=limit)
	return patients

@app.get("/pharmacies", response_model=List[schemas.Patient])
async def read_pharmacies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: User = Depends(utils.get_current_user)):
	pharmacies = utils.get_pharmacies(db, skip=skip, limit=limit)
	return pharmacies

@app.get("/transactions", response_model=List[schemas.Transaction])
async def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: User = Depends(utils.get_current_user)):
	transactions = utils.get_transactions(db, skip=skip, limit=limit)
	return transactions