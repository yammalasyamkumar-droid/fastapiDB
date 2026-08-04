from pydantic import BaseModel
class HospitalCreate(BaseModel):
    name: str
    department:str 
    location:str
    address:str


class HospitalResponse(HospitalCreate):
    id: int

    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    name:str
    email:str
    password:str


class UserResponse(UserCreate):
    id: int

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email:str
    password:str