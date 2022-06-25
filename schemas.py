from pydantic import BaseModel

class Patients(BaseModel):
    uuid: str
    first_name: str = None
    last_name: str = None
    date_of_birth: str = None
    
    class Config:
        orm_mode = True

class Pharmacies(BaseModel):
    uuid: str
    name: str = None
    city: str = None
    
    class Config:
        orm_mode = True

class Transactions(BaseModel):
    uuid: str
    patient_uuid: str = None
    pharmacy_uuid: str = None
    amount: str = None
    timestamp: str = None

    class Config:
        orm_mode = True


