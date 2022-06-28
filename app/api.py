
from datetime import timedelta
from fastapi import Depends, FastAPI, Body
from typing import List
from app.database.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User
import app.schemas as schemas
from decouple import config
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth import AuthHandler
import app.utils as utils
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder

app = FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")
auth_handler = AuthHandler()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.post('/token')
def login(auth_details: schemas.AuthDetails, db: Session = Depends(get_db)):
	user = None
	users = utils.get_users(db)
	for x in users:
		if x.username == auth_details.username:
			user = x
			break
	
	if (user is None) or (not utils.verify_password(auth_details.password, user.password)):
		raise HTTPException(status_code=401, detail='Invalid username and/or password')
	token = auth_handler.encode_token(user.username)
	return { 'token': token }

class UserRead(User):
    uuid: str

@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	users = utils.get_users(db, skip=skip, limit=limit)
	return users

@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = utils.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return utils.create_user(db=db, user=user)

@app.get("/patients", response_model=List[schemas.Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	patients = utils.get_patients(db, skip=skip, limit=limit)
	return patients

@app.get("/pharmacies", response_model=List[schemas.Patient])
def read_pharmacies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	pharmacies = utils.get_pharmacies(db, skip=skip, limit=limit)
	return pharmacies

@app.get("/transactions", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	transactions = utils.get_transactions(db, skip=skip, limit=limit)
	return transactions