from pydantic import BaseModel
from typing import Optional, Union


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in_minutes: str


class AuthDetails(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    uuid: str
    username: str = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserUpdate(BaseModel):
    uuid: Optional[str]
    username: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True


class Patient(BaseModel):
    uuid: str
    first_name: str = None
    last_name: str = None
    date_of_birth: str = None

    class Config:
        orm_mode = True


class Pharmacy(BaseModel):
    uuid: str
    name: str = None
    city: str = None

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    patient: Patient = None
    pharmacy: Pharmacy = None
    uuid: str
    amount: str = None
    timestamp: str = None
    patient: Patient = None

    class Config:
        orm_mode = True
