from sqlalchemy.orm import Session
import hashlib
from app.database.database import get_db
import app.models as models
import app.schemas as schemas
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union
from decouple import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        uuid=user.uuid,
        username=user.username,
        password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_patients(
    db: Session,
    first_name: str = None,
    last_name: str = None,
    skip: int = 0,
    limit: int = 100,
):
    if first_name and last_name:
        return (
            db.query(models.Patient)
            .filter(models.Patient.first_name == first_name)
            .filter(models.Patient.last_name == last_name)
            .offset(skip)
            .limit(limit)
            .all()
        )
    elif first_name:
        return (
            db.query(models.Patient)
            .filter(models.Patient.first_name == first_name)
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        return db.query(models.Patient).offset(skip).limit(limit).all()


def get_pharmacies(db: Session, name: str = None, skip: int = 0, limit: int = 100):
    if name:
        return (
            db.query(models.Pharmacy)
            .filter(models.Pharmacy.name == name)
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        return db.query(models.Pharmacy).offset(skip).limit(limit).all()


def get_pharmacy(db: Session, name: str = None):
    return db.query(models.Pharmacy).filter(models.Pharmacy.name == name).first()


def get_patient(db: Session, patient_name: str = None):
    patient_name = patient_name.split(" ")
    first_name = patient_name[0]
    last_name = patient_name[1]
    return (
        db.query(models.Patient)
        .filter(models.Patient.first_name == first_name)
        .filter(models.Patient.last_name == last_name)
        .first()
    )


def get_transactions(
    db: Session,
    patient_name: str = None,
    pharmacy_name: str = None,
    skip: int = 0,
    limit: int = 100,
):

    if patient_name and pharmacy_name:

        patient = get_patient(db, patient_name)
        pharmacy = get_pharmacy(db, pharmacy_name)

        return (
            db.query(models.Transaction)
            .filter(models.Transaction.patient == patient)
            .filter(models.Transaction.pharmacy == pharmacy)
            .all()
        )

    if pharmacy_name:
        pharmacy = get_pharmacy(db, pharmacy_name)

        return (
            db.query(models.Transaction)
            .filter(models.Transaction.pharmacy == pharmacy)
            .all()
        )

    if patient_name:
        patient = get_patient(db, patient_name)

        return (
            db.query(models.Transaction)
            .filter(models.Transaction.patient == patient)
            .all()
        )

    return db.query(models.Transaction).offset(skip).limit(limit).all()


def hash_password(password: str):
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    db_user = get_user_by_username(db=db, username=username)

    if username and db_user and username == db_user.username:
        return db_user


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False

    if password == user.password:
        return user

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
