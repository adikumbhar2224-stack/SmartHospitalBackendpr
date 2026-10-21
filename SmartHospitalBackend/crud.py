from sqlalchemy.orm import Session
from sqlalchemy import func

from models import (
    User,
    Patient,
    Doctor,
    Department,
    Token,
    QueueHistory
)

from auth import hash_password


# =====================================================
# PATIENT
# =====================================================

def create_patient(
    db: Session,
    data
):

    user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password),
        role="patient"
    )

    db.add(user)
    db.flush()

    patient = Patient(
        user_id=user.user_id,
        patient_name=data.patient_name,
        age=data.age,
        gender=data.gender,
        phone=data.phone,
        email=data.email,
        department_id=data.department_id,
        doctor_id=data.doctor_id
    )

    db.add(patient)

    db.commit()
    db.refresh(patient)

    return patient


def get_patients(db: Session):

    return db.query(Patient).all()


def get_patient(
    db: Session,
    patient_id: int
):

    return db.query(Patient).filter(
        Patient.patient_id == patient_id
    ).first()


# =====================================================
# DOCTOR
# =====================================================

def create_doctor(
    db: Session,
    data
):

    user = User(
        username=data.username,
        email=data.email or f"{data.username}@hospital.com",
        password=hash_password(data.password),
        role="doctor"
    )

    db.add(user)
    db.flush()

    doctor = Doctor(
        user_id=user.user_id,
        doctor_name=data.doctor_name,
        specialization=data.specialization,
        department_id=data.department_id,
        phone=data.phone,
        email=data.email,
        qualification=data.qualification,
        experience=data.experience
    )

    db.add(doctor)

    db.commit()
    db.refresh(doctor)

    return doctor


def get_doctors(db: Session):

    return db.query(Doctor).all()


def get_doctor(
    db: Session,
    doctor_id: int
):

    return db.query(Doctor).filter(
        Doctor.doctor_id == doctor_id
    ).first()


def delete_doctor(
    db: Session,
    doctor_id: int
):

    doctor = get_doctor(db, doctor_id)

    if not doctor:
        return False

    user = db.query(User).filter(
        User.user_id == doctor.user_id
    ).first()

    db.delete(doctor)

    if user:
        db.delete(user)

    db.commit()

    return True


# =====================================================
# DEPARTMENT
# =====================================================

def create_department(
    db: Session,
    data
):

    department = Department(
        department_name=data.department_name,
        description=data.description
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


def get_departments(db: Session):

    return db.query(Department).all()


# =====================================================
# TOKEN
# =====================================================

def generate_token(
    db: Session,
    patient_id: int
):

    patient = get_patient(
        db,
        patient_id
    )

    if not patient:
        return None

    today = func.current_date()

    count = db.query(Token).filter(
        Token.doctor_id == patient.doctor_id,
        Token.token_date == today
    ).count()

    queue_position = count + 1

    token_number = (
        f"D-{queue_position:03d}"
    )

    token = Token(
        token_number=token_number,
        patient_id=patient.patient_id,
        doctor_id=patient.doctor_id,
        department_id=patient.department_id,
        queue_position=queue_position,
        status="Waiting"
    )

    db.add(token)

    db.commit()
    db.refresh(token)

    history = QueueHistory(
        token_id=token.token_id,
        patient_id=token.patient_id,
        doctor_id=token.doctor_id,
        department_id=token.department_id,
        token_number=token.token_number,
        status="Waiting",
        action_by="patient",
        remarks="Token generated"
    )

    db.add(history)

    db.commit()

    return token


def get_patient_tokens(
    db: Session,
    patient_id: int
):

    return db.query(Token).filter(
        Token.patient_id == patient_id
    ).order_by(
        Token.generated_at.desc()
    ).all()


# =====================================================
# DOCTOR QUEUE
# =====================================================

def get_doctor_queue(
    db: Session,
    doctor_id: int
):

    return db.query(Token).filter(
        Token.doctor_id == doctor_id
    ).order_by(
        Token.queue_position
    ).all()


# =====================================================
# CALL NEXT
# =====================================================

def call_next_patient(
    db: Session,
    doctor_id: int
):

    current = db.query(Token).filter(
        Token.doctor_id == doctor_id,
        Token.status == "Now Serving"
    ).first()

    if current:

        current.status = "Completed"

        history = QueueHistory(
            token_id=current.token_id,
            patient_id=current.patient_id,
            doctor_id=current.doctor_id,
            department_id=current.department_id,
            token_number=current.token_number,
            status="Completed",
            action_by="admin",
            remarks="Patient completed"
        )

        db.add(history)

    next_token = db.query(Token).filter(
        Token.doctor_id == doctor_id,
        Token.status == "Waiting"
    ).order_by(
        Token.queue_position
    ).first()

    if not next_token:

        db.commit()

        return None

    next_token.status = "Now Serving"

    history = QueueHistory(
        token_id=next_token.token_id,
        patient_id=next_token.patient_id,
        doctor_id=next_token.doctor_id,
        department_id=next_token.department_id,
        token_number=next_token.token_number,
        status="Now Serving",
        action_by="admin",
        remarks="Called next patient"
    )

    db.add(history)

    db.commit()
    db.refresh(next_token)

    return next_token