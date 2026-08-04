from sqlalchemy.orm import Session
import models
import schemas
import bcrypt
from fastapi import HTTPException, Response
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"


# =====================================================
#                   PATIENT CRUD
# =====================================================

def create_patient(db: Session, patient: schemas.HospitalCreate):
    db_patient = models.Hospital(
        name=patient.name,
        department=patient.department,
        location=patient.location,
        address=patient.address
    )

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient


def get_patients(db: Session):
    return db.query(models.Hospital).all()


def get_patient(db: Session, patient_id: int):
    return (
        db.query(models.Hospital)
        .filter(models.Hospital.id == patient_id)
        .first()
    )


def update_patient(db: Session, patient_id: int, patient: schemas.HospitalCreate):

    db_patient = get_patient(db, patient_id)

    if not db_patient:
        return None

    db_patient.name = patient.name
    db_patient.department = patient.department
    db_patient.location = patient.location
    db_patient.address = patient.address

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


def get_patient_by_dept(db: Session, dept: str):

    return (
        db.query(models.Hospital)
        .filter(models.Hospital.department == dept)
        .all()
    )


# =====================================================
#                   USER CRUD
# =====================================================

def create_user(user: schemas.UserCreate, db: Session):

    existing_user = (
        db.query(models.Users)
        .filter(models.Users.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt(rounds=13)
    ).decode("utf-8")

    db_user = models.Users(
        name=user.name,
        email=user.email,
        password=hashed_password,

        # Every registered user is NORMAL USER
        is_admin=False,

        is_active=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(user: schemas.UserLogin,
               db: Session,
               response: Response):

    db_user = (
        db.query(models.Users)
        .filter(models.Users.email == user.email)
        .first()
    )

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    valid = bcrypt.checkpw(
        user.password.encode("utf-8"),
        db_user.password.encode("utf-8")
    )

    if not valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    payload = {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "is_admin": db_user.is_admin,
        "is_loggedin": True,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return {
        "message": "Login Successful",
        "access_token": token,
        "is_admin": db_user.is_admin
    }


# =====================================================
#                 USER HELPERS
# =====================================================

def get_user_by_id(db: Session, user_id: int):

    return (
        db.query(models.Users)
        .filter(models.Users.id == user_id)
        .first()
    )


def get_all_users(db: Session):

    return db.query(models.Users).all()