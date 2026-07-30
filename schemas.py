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