from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.database import get_db
from app.models.church import Member, GivingRecord, GivingCategory
from app.schemas.church import MemberCreate, MemberOut, GivingRecordOut
from typing import List, Optional
from sqlalchemy.orm import selectinload

router = APIRouter()

@router.post("/", response_model=MemberOut, status_code=201)
async def create_member(data: MemberCreate, db: AsyncSession = Depends(get_db)):
    member = Member(**data.model_dump())
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member

@router.get("/", response_model=List[MemberOut])
async def list_members(
    church_id: str = None,
    branch_id: str = None,
    search: str = None,
    db: AsyncSession = Depends(get_db)
):
    q = select(Member).where(Member.is_deleted == False)
    if church_id:
        q = q.where(Member.church_id == church_id)
    if branch_id:
        q = q.where(Member.branch_id == branch_id)
    if search:
        q = q.where(or_(
            Member.first_name.ilike(f"%{search}%"),
            Member.last_name.ilike(f"%{search}%"),
            Member.phone.ilike(f"%{search}%"),
            Member.email.ilike(f"%{search}%"),
        ))
    q = q.order_by(Member.first_name)
    result = await db.execute(q)
    return result.scalars().all()

@router.get("/{member_id}", response_model=MemberOut)
async def get_member(member_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Member).where(Member.id == member_id))
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@router.get("/{member_id}/giving", response_model=List[GivingRecordOut])
async def get_member_giving(member_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GivingRecord)
        .options(selectinload(GivingRecord.category))
        .where(GivingRecord.member_id == member_id)
        .order_by(GivingRecord.created_at.desc())
    )
    records = result.scalars().all()
    out = []
    for r in records:
        d = {
            "id": r.id, "church_id": r.church_id, "branch_id": r.branch_id,
            "member_id": r.member_id, "session_id": r.session_id,
            "category_id": r.category_id, "amount_kes": r.amount_kes,
            "payment_method": r.payment_method, "mpesa_ref": r.mpesa_ref,
            "envelope_number": r.envelope_number, "notes": r.notes,
            "created_at": r.created_at,
            "member_name": None,
            "category_name": r.category.name if r.category else None,
        }
        out.append(d)
    return out

@router.put("/{member_id}", response_model=MemberOut)
async def update_member(member_id: str, data: MemberCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Member).where(Member.id == member_id))
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    for k, v in data.model_dump().items():
        setattr(member, k, v)
    await db.commit()
    await db.refresh(member)
    return member
