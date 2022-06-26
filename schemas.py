from pydantic import BaseModel

class User(BaseModel):
    uuid: str
    username: str = None
    password: str = None
    
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


