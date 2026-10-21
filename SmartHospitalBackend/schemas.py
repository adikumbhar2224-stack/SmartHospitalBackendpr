from pydantic import BaseModel, EmailStr
from typing import Optional


# =========================
# LOGIN
# =========================

class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    role: str


# =========================
# PATIENT
# =========================

class PatientCreate(BaseModel):
    username: str
    password: str

    patient_name: str
    age: int
    gender: str

    phone: str
    email: EmailStr

    department_id: int
    doctor_id: int


class PatientResponse(BaseModel):
    patient_id: int
    user_id: Optional[int]
    patient_name: str
    age: int
    gender: str
    phone: str
    email: str
    department_id: int
    doctor_id: int

    class Config:
        from_attributes = True


# =========================
# DOCTOR
# =========================

class DoctorCreate(BaseModel):
    username: str
    password: str

    doctor_name: str
    specialization: Optional[str] = None

    department_id: int

    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    qualification: Optional[str] = None
    experience: Optional[int] = None


class DoctorResponse(BaseModel):
    doctor_id: int
    user_id: Optional[int]

    doctor_name: str
    specialization: Optional[str]

    department_id: int

    phone: Optional[str]
    email: Optional[str]

    qualification: Optional[str]
    experience: Optional[int]

    status: str

    class Config:
        from_attributes = True


# =========================
# DEPARTMENT
# =========================

class DepartmentCreate(BaseModel):
    department_name: str
    description: Optional[str] = None


class DepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    description: Optional[str]
    status: str

    class Config:
        from_attributes = True


# =========================
# TOKEN
# =========================

class TokenCreate(BaseModel):
    patient_id: int


class TokenResponse(BaseModel):
    token_id: int
    token_number: str
    patient_id: int
    doctor_id: int
    department_id: int
    queue_position: Optional[int]
    status: str

    class Config:
        from_attributes = True