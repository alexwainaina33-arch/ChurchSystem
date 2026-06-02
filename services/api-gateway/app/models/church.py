import uuid
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, Numeric, Text, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
import enum

class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class MembershipStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    visitor = "visitor"
    transferred = "transferred"

class PaymentMethod(str, enum.Enum):
    cash = "cash"
    mpesa = "mpesa"
    bank_transfer = "bank_transfer"
    cheque = "cheque"

class SessionType(str, enum.Enum):
    sunday_service = "sunday_service"
    midweek = "midweek"
    special = "special"

class ProjectStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    paused = "paused"

class MessageChannel(str, enum.Enum):
    sms = "sms"
    whatsapp = "whatsapp"
    email = "email"
    in_app = "in_app"

# ── Church ──────────────────────────────────────────────
class Church(BaseModel):
    __tablename__ = "churches"
    name: Mapped[str] = mapped_column(String(200))
    denomination: Mapped[Optional[str]] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100), default="Kenya")
    city: Mapped[Optional[str]] = mapped_column(String(100))
    address: Mapped[Optional[str]] = mapped_column(Text)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    branches: Mapped[List["Branch"]] = relationship("Branch", back_populates="church")
    members: Mapped[List["Member"]] = relationship("Member", back_populates="church")
    accounts: Mapped[List["Account"]] = relationship("Account", back_populates="church")

# ── Branch ───────────────────────────────────────────────
class Branch(BaseModel):
    __tablename__ = "branches"
    church_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("churches.id"))
    name: Mapped[str] = mapped_column(String(200))
    address: Mapped[Optional[str]] = mapped_column(Text)
    pastor_name: Mapped[Optional[str]] = mapped_column(String(200))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    church: Mapped["Church"] = relationship("Church", back_populates="branches")
    members: Mapped[List["Member"]] = relationship("Member", back_populates="branch")
    sessions: Mapped[List["AttendanceSession"]] = relationship("AttendanceSession", back_populates="branch")

# ── Member ───────────────────────────────────────────────
class Member(BaseModel):
    __tablename__ = "members"
    church_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("churches.id"))
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("branches.id"))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[Optional[str]] = mapped_column(String(200))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date)
    gender: Mapped[Optional[str]] = mapped_column(String(10))
    marital_status: Mapped[Optional[str]] = mapped_column(String(20))
    membership_status: Mapped[str] = mapped_column(String(20), default="active")
    membership_date: Mapped[Optional[date]] = mapped_column(Date)
    baptism_date: Mapped[Optional[date]] = mapped_column(Date)
    occupation: Mapped[Optional[str]] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    church: Mapped["Church"] = relationship("Church", back_populates="members")
    branch: Mapped[Optional["Branch"]] = relationship("Branch", back_populates="members")
    giving_records: Mapped[List["GivingRecord"]] = relationship("GivingRecord", back_populates="member")

# ── Attendance Session ────────────────────────────────────
class AttendanceSession(BaseModel):
    __tablename__ = "attendance_sessions"
    church_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("churches.id"))
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("branches.id"))
    session_date: Mapped[date] = mapped_column(Date)
    session_type: Mapped[str] = mapped_column(String(30), default="sunday_service")
    service_name: Mapped[Optional[str]] = mapped_column(String(200))
    total_count: Mapped[int] = mapped_column(Integer, default=0)
    adult_count: Mapped[int] = mapped_column(Integer, default=0)
    child_count: Mapped[int] = mapped_column(Integer, default=0)
    male_count: Mapped[int] = mapped_column(Integer, default=0)
    female_count: Mapped[int] = mapped_column(Integer, default=0)
    first_time_visitors: Mapped[int] = mapped_column(Integer, default=0)
    salvations: Mapped[int] = mapped_column(Integer, default=0)
    cars_count: Mapped[int] = mapped_column(Integer, default=0)
    motorbikes_count: Mapped[int] = mapped_column(Integer, default=0)
    total_offering_kes: Mapped[int] = mapped_column(Integer, default=0)
    total_tithe_kes: Mapped[int] = mapped_column(Integer, default=0)
    project_offering_kes: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    branch: Mapped[Optional["Branch"]] = relationship("Branch", back_populates="sessions")
    giving_records: Mapped[List["GivingRecord"]] = relationship("GivingRecord", back_populates="session")

# ── Giving Category ───────────────────────────────────────
class GivingCategory(BaseModel):
    __tablename__ = "giving_categories"
    church_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("churches.id"))
    name: Mapped[str] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(20))
    gl_debit_code: Mapped[str] = mapped_column(String(20), default="1000")
    gl_credit_code: Mapped[str] = mapped_column(String(20), default="4000")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    giving_records: Mapped[List["GivingRecord"]] = relationship("GivingRecord", back_populates="category")

# ── Giving Record ─────────────────────────────────────────
class GivingRecord(BaseModel):
    __tablename__ = "giving_records"
    church_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("churches.id"))
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("branches.id"))
    member_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("members.id"))
    session_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("attendance_sessions.id"))
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("giving_categories.id"))
    amount_kes: Mapped[int] = mapped_column(Integer)
    payment_method: Mapped[str] = mapped_column(String(20), default="cash")
    mpesa_ref: Mapped[Optional[str]] = mapped_column(String(50))
    envelope_number: Mapped[Optional[str]] = mapped_column(String(20))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    member: Mapped[Optional["Member"]] = relationship("Member", back_populates="giving_records")
    category: Mapped["GivingCategory"] = relationship("GivingCategory", back_populates="giving_records")
    session: Mapped[Optional["AttendanceSession"]] = relationship("AttendanceSession", back_populates="giving_records")

# ── GL Accounts ───────────────────────────────────────────
class Account(BaseModel):
    __tablename__ = "accounts"
    church_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("churches.id"))
    code: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(200))
    type: Mapped[str] = mapped_column(String(20))
    balance: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    church: Mapped["Church"] = relationship("Church", back_populates="accounts")

# ── GL Transactions ───────────────────────────────────────
class Transaction(BaseModel):
    __tablename__ = "transactions"
    church_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("churches.id"))
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("branches.id"))
    debit_account_code: Mapped[str] = mapped_column(String(20))
    credit_account_code: Mapped[str] = mapped_column(String(20))
    amount: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(500))
    event_type: Mapped[str] = mapped_column(String(50))
    idempotency_key: Mapped[str] = mapped_column(String(200), unique=True)
    reference_id: Mapped[Optional[str]] = mapped_column(String(200))

# ── Projects ──────────────────────────────────────────────
class Project(BaseModel):
    __tablename__ = "projects"
    church_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("churches.id"))
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("branches.id"))
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text)
    target_amount_kes: Mapped[int] = mapped_column(Integer, default=0)
    collected_amount_kes: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="active")

# ── Messages ──────────────────────────────────────────────
class Message(BaseModel):
    __tablename__ = "messages"
    church_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("churches.id"))
    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("branches.id"))
    subject: Mapped[str] = mapped_column(String(300))
    body: Mapped[str] = mapped_column(Text)
    channel: Mapped[str] = mapped_column(String(20), default="in_app")
    audience: Mapped[str] = mapped_column(String(50), default="all")
    status: Mapped[str] = mapped_column(String(20), default="sent")
