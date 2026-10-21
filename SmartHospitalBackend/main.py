from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import (
    engine,
    Base,
    get_db
)

import models
import crud

from schemas import (
    LoginRequest,
    LoginResponse,

    PatientCreate,
    PatientResponse,

    DoctorCreate,
    DoctorResponse,

    DepartmentCreate,
    DepartmentResponse,

    TokenCreate,
    TokenResponse
)

from auth import (
    verify_password,
    create_access_token
)


# =====================================================
# CREATE DATABASE TABLES
# =====================================================

Base.metadata.create_all(
    bind=engine
)


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="Smart Hospital Queue Management System",
    version="1.0"
)


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def home():

    return {
        "message":
        "Smart Hospital Queue API is running"
    }


# =====================================================
# LOGIN
# =====================================================

@app.post(
    "/login",
    response_model=LoginResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(
        models.User
    ).filter(
        models.User.username ==
        data.username
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        data.password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        {
            "user_id": user.user_id,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }


# =====================================================
# DEPARTMENT MANAGEMENT
# =====================================================

@app.post(
    "/departments",
    response_model=DepartmentResponse
)
def add_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db)
):

    return crud.create_department(
        db,
        data
    )


@app.get(
    "/departments",
    response_model=list[DepartmentResponse]
)
def get_departments(
    db: Session = Depends(get_db)
):

    return crud.get_departments(db)


# =====================================================
# DOCTOR MANAGEMENT
# =====================================================

@app.post(
    "/doctors",
    response_model=DoctorResponse
)
def add_doctor(
    data: DoctorCreate,
    db: Session = Depends(get_db)
):

    return crud.create_doctor(
        db,
        data
    )


@app.get(
    "/doctors",
    response_model=list[DoctorResponse]
)
def get_doctors(
    db: Session = Depends(get_db)
):

    return crud.get_doctors(db)


@app.get(
    "/doctors/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    doctor = crud.get_doctor(
        db,
        doctor_id
    )

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@app.delete(
    "/doctors/{doctor_id}"
)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    result = crud.delete_doctor(
        db,
        doctor_id
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return {
        "message":
        "Doctor deleted successfully"
    }


# =====================================================
# PATIENT MANAGEMENT
# =====================================================

@app.post(
    "/patients",
    response_model=PatientResponse
)
def add_patient(
    data: PatientCreate,
    db: Session = Depends(get_db)
):

    return crud.create_patient(
        db,
        data
    )


@app.get(
    "/patients",
    response_model=list[PatientResponse]
)
def get_patients(
    db: Session = Depends(get_db)
):

    return crud.get_patients(db)


@app.get(
    "/patients/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = crud.get_patient(
        db,
        patient_id
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


# =====================================================
# GET TOKEN
# =====================================================

@app.post(
    "/tokens",
    response_model=TokenResponse
)
def get_token(
    data: TokenCreate,
    db: Session = Depends(get_db)
):

    token = crud.generate_token(
        db,
        data.patient_id
    )

    if not token:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return token


# =====================================================
# PATIENT QUEUE STATUS
# =====================================================

@app.get(
    "/patients/{patient_id}/tokens",
    response_model=list[TokenResponse]
)
def patient_queue_status(
    patient_id: int,
    db: Session = Depends(get_db)
):

    return crud.get_patient_tokens(
        db,
        patient_id
    )


# =====================================================
# DOCTOR QUEUE
# =====================================================

@app.get(
    "/doctors/{doctor_id}/queue"
)
def doctor_queue(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    tokens = crud.get_doctor_queue(
        db,
        doctor_id
    )

    return {
        "total_patients": len(tokens),

        "completed": len([
            t for t in tokens
            if t.status == "Completed"
        ]),

        "pending": len([
            t for t in tokens
            if t.status == "Waiting"
        ]),

        "patients": tokens
    }


# =====================================================
# ADMIN CALL NEXT
# =====================================================

@app.post(
    "/admin/call-next/{doctor_id}",
    response_model=TokenResponse
)
def call_next(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    token = crud.call_next_patient(
        db,
        doctor_id
    )

    if not token:

        raise HTTPException(
            status_code=404,
            detail="No waiting patient"
        )

    return token


# =====================================================
# QUEUE HISTORY
# =====================================================

@app.get(
    "/queue-history"
)
def queue_history(
    db: Session = Depends(get_db)
):

    return db.query(
        models.QueueHistory
    ).order_by(
        models.QueueHistory.action_time.desc()
    ).all()