from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

# ── Church ──────────────────────────────────────────────
class ChurchCreate(BaseModel):
    name: str
    denomination: Optional[str] = None
    country: str = "Kenya"
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class ChurchOut(ChurchCreate):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

# ── Branch ───────────────────────────────────────────────
class BranchCreate(BaseModel):
    church_id: UUID
    name: str
    address: Optional[str] = None
    pastor_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class BranchOut(BranchCreate):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

# ── Member ───────────────────────────────────────────────
class MemberCreate(BaseModel):
    church_id: UUID
    branch_id: Optional[UUID] = None
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    membership_status: str = "active"
    membership_date: Optional[date] = None
    baptism_date: Optional[date] = None
    occupation: Optional[str] = None

class MemberOut(MemberCreate):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

# ── Attendance ───────────────────────────────────────────
class AttendanceCreate(BaseModel):
    church_id: UUID
    branch_id: Optional[UUID] = None
    session_date: date
    session_type: str = "sunday_service"
    service_name: Optional[str] = None
    total_count: int = 0
    adult_count: int = 0
    child_count: int = 0
    male_count: int = 0
    female_count: int = 0
    first_time_visitors: int = 0
    salvations: int = 0
    cars_count: int = 0
    motorbikes_count: int = 0
    total_offering_kes: int = 0
    total_tithe_kes: int = 0
    project_offering_kes: int = 0
    notes: Optional[str] = None

class AttendanceOut(AttendanceCreate):
    id: UUID
    created_at: datetime
    branch_name: Optional[str] = None
    class Config:
        from_attributes = True

# ── Giving ────────────────────────────────────────────────
class GivingCategoryCreate(BaseModel):
    church_id: UUID
    name: str
    code: str
    gl_debit_code: str = "1000"
    gl_credit_code: str = "4000"

class GivingCategoryOut(GivingCategoryCreate):
    id: UUID
    class Config:
        from_attributes = True

class GivingRecordCreate(BaseModel):
    church_id: UUID
    branch_id: Optional[UUID] = None
    member_id: Optional[UUID] = None
    session_id: Optional[UUID] = None
    category_id: UUID
    amount_kes: int
    payment_method: str = "cash"
    mpesa_ref: Optional[str] = None
    envelope_number: Optional[str] = None
    notes: Optional[str] = None

class GivingRecordOut(GivingRecordCreate):
    id: UUID
    created_at: datetime
    member_name: Optional[str] = None
    category_name: Optional[str] = None
    class Config:
        from_attributes = True

# ── Project ───────────────────────────────────────────────
class ProjectCreate(BaseModel):
    church_id: UUID
    branch_id: Optional[UUID] = None
    name: str
    description: Optional[str] = None
    target_amount_kes: int = 0
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class ProjectOut(ProjectCreate):
    id: UUID
    collected_amount_kes: int
    status: str
    progress_percent: Optional[float] = None
    created_at: datetime
    class Config:
        from_attributes = True

# ── Message ───────────────────────────────────────────────
class MessageCreate(BaseModel):
    church_id: UUID
    branch_id: Optional[UUID] = None
    subject: str
    body: str
    channel: str = "in_app"
    audience: str = "all"

class MessageOut(MessageCreate):
    id: UUID
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

# ── Dashboard ─────────────────────────────────────────────
class BranchDashboard(BaseModel):
    branch_id: UUID
    branch_name: str
    total_members: int
    total_tithe_this_month: int
    total_offering_this_month: int
    last_sunday_attendance: int
    active_projects: int
