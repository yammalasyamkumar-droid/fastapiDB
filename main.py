from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/patients", response_model=schemas.HospitalResponse)
def create(patient: schemas.HospitalCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

@app.get("/patients", response_model=list[schemas.HospitalResponse])
def read_all(db: Session = Depends(get_db)):
    return crud.get_patients(db)

@app.get("/patients/{patient_id}", response_model=schemas.HospitalResponse)
def read_one(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return patient

@app.put("/patients/{patient_id}", response_model=schemas.HospitalResponse)
def update(patient_id: int, patient: schemas.HospitalCreate, db: Session = Depends(get_db)):
    updated = crud.update_patient(db, patient_id, patient)
    if not updated:
        raise HTTPException(status_code=404, detail="patient not found")
    return updated

@app.delete("/patients/{patient_id}")
def delete(patient_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_patient(db, patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="patient not found")
    return {"message":"patient deleted successfully"}




@app.get("/dept/{dept}")
def get_dept_patient(dept:str,db:Session=Depends(get_db)):
    return crud.get_patient_by_dept(db,dept)