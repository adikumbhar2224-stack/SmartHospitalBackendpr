from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.sql import func
from database import Base


# =========================
# USERS
# =========================

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# =========================
# DEPARTMENTS
# =========================

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    department_name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    description = Column(Text)

    status = Column(
        String(20),
        default="Active"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# =========================
# DOCTORS
# =========================

class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        unique=True,
        nullable=True
    )

    doctor_name = Column(
        String(150),
        nullable=False
    )

    specialization = Column(
        String(150)
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id"),
        nullable=False
    )

    phone = Column(String(15))

    email = Column(String(150))

    qualification = Column(String(150))

    experience = Column(Integer)

    status = Column(
        String(20),
        default="Active"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# =========================
# PATIENTS
# =========================

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        unique=True,
        nullable=True
    )

    patient_name = Column(
        String(150),
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    gender = Column(
        String(20),
        nullable=False
    )

    phone = Column(
        String(15),
        unique=True,
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id"),
        nullable=False
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.doctor_id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# =========================
# TOKENS
# =========================

class Token(Base):
    __tablename__ = "tokens"

    token_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    token_number = Column(
        String(20),
        unique=True,
        nullable=False
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.patient_id"),
        nullable=False
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.doctor_id"),
        nullable=False
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id"),
        nullable=False
    )

    queue_position = Column(Integer)

    status = Column(
        String(30),
        default="Waiting"
    )

    token_date = Column(
        Date,
        server_default=func.current_date()
    )

    generated_at = Column(
        DateTime,
        server_default=func.now()
    )

    called_at = Column(DateTime)

    completed_at = Column(DateTime)


# =========================
# QUEUE HISTORY
# =========================

class QueueHistory(Base):
    __tablename__ = "queue_history"

    history_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    token_id = Column(
        Integer,
        ForeignKey("tokens.token_id"),
        nullable=False
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.patient_id"),
        nullable=False
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.doctor_id"),
        nullable=False
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.department_id"),
        nullable=False
    )

    token_number = Column(
        String(20),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False
    )

    action_time = Column(
        DateTime,
        server_default=func.now()
    )

    action_by = Column(String(20))

    remarks = Column(Text)