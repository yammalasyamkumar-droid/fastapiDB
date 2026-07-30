from sqlalchemy.orm import Session
import models
import schemas

def create_patient(db: Session, patient: schemas.HospitalCreate):
    #creating  a patient object with user values
    db_patient = models.Hospital(**patient.model_dump())
    #adding new patient to existing table
    db.add(db_patient)
    #commiting the changes to the database
    db.commit()
    #refreshing the database to get updated values
    db.refresh(db_patient)
    #returning response to the user
    return db_patient

def get_patients(db: Session):
    return db.query(models.Hospital).all()

def get_patient(db: Session, patient_id: int):
    return db.query(models.Hospital).filter(
        models.Hospital.id == patient_id
    ).first()

def update_patient(db: Session, patient_id: int, patient: schemas.HospitalCreate):
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None
    db_patient.name = patient.name
    db_patient.department=patient.department 
    db_patient.address=patient.address
    db_patient.location=patient.location

    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None
    db.delete(db_patient)
    db.commit()
    return db_patient



def get_patient_by_dept(db:Session,dept:str):
    print(dept)
    return db.query(models.Hospital).filter(
        models.Hospital.department==dept
    ).all()