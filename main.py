from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session

import crud
import schemas
import models

from database import Base, engine, SessionLocal
from auth import get_current_user, verify_admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management API")


# ===============================
# Database Dependency
# ===============================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===============================
# Home
# ===============================

@app.get("/")
def home():
    return {
        "message": "Welcome to Hospital Management API"
    }


# ===============================
# User Authentication
# ===============================

@app.post("/users/register", response_model=schemas.UserResponse)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(user, db)


@app.post("/users/login")
def login_user(
    response: Response,
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    return crud.login_user(user, db, response)


# ===============================
# User Profile
# ===============================

@app.get("/users/me", response_model=schemas.UserResponse)
def my_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user = crud.get_user_by_id(db, current_user["id"])

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    if (
        current_user["is_admin"] is not True
        and current_user["id"] != user_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    user = crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin: dict = Depends(verify_admin)
):
    return crud.get_all_users(db)


# ===============================
# Patient APIs
# Admin Only
# ===============================

@app.post("/patients", response_model=schemas.HospitalResponse)
def create_patient(
    patient: schemas.HospitalCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(verify_admin)
):
    return crud.create_patient(db, patient)


@app.get("/patients", response_model=list[schemas.HospitalResponse])
def get_all_patients(
    db: Session = Depends(get_db),
    admin: dict = Depends(verify_admin)
):
    return crud.get_patients(db)


@app.get("/patients/{patient_id}", response_model=schemas.HospitalResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(verify_admin)
):
    patient = crud.get_patient(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


@app.put("/patients/{patient_id}", response_model=schemas.HospitalResponse)
def update_patient(
    patient_id: int,
    patient: schemas.HospitalCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(verify_admin)
):
    updated = crud.update_patient(db, patient_id, patient)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return updated


@app.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(verify_admin)
):
    deleted = crud.delete_patient(db, patient_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return {
        "message": "Patient deleted successfully"
    }


@app.get("/patients/dept/{dept}", response_model=list[schemas.HospitalResponse])
def get_department_patients(
    dept: str,
    db: Session = Depends(get_db),
    admin: dict = Depends(verify_admin)
):
    return crud.get_patient_by_dept(db, dept)