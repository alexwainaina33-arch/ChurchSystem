from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.church import GivingRecord, GivingCategory, Member, Account, Transaction
from app.schemas.church import GivingRecordCreate, GivingRecordOut, GivingCategoryCreate, GivingCategoryOut
from typing import List, Optional
import uuid

router = APIRouter()

async def post_gl(db, church_id, branch_id, debit_code, credit_code, amount, description, event_type, idempotency_key):
    existing = await db.execute(select(Transaction).where(Transaction.idempotency_key == idempotency_key))
    if existing.scalar_one_or_none():
        return
    txn = Transaction(
        church_id=church_id,
        branch_id=branch_id,
        debit_account_code=debit_code,
        credit_account_code=credit_code,
        amount=amount,
        description=description,
        event_type=event_type,
        idempotency_key=idempotency_key,
    )
    db.add(txn)
    dr = await db.execute(select(Account).where(Account.church_id == church_id, Account.code == debit_code))
    dr_acct = dr.scalar_one_or_none()
    if dr_acct:
        dr_acct.balance += amount
    cr = await db.execute(select(Account).where(Account.church_id == church_id, Account.code == credit_code))
    cr_acct = cr.scalar_one_or_none()
    if cr_acct:
        cr_acct.balance += amount

@router.post("/categories/", response_model=GivingCategoryOut, status_code=201)
async def create_category(data: GivingCategoryCreate, db: AsyncSession = Depends(get_db)):
    cat = GivingCategory(**data.model_dump())
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat

@router.get("/categories/", response_model=List[GivingCategoryOut])
async def list_categories(church_id: str = None, db: AsyncSession = Depends(get_db)):
    q = select(GivingCategory).where(GivingCategory.is_deleted == False)
    if church_id:
        q = q.where(GivingCategory.church_id == church_id)
    result = await db.execute(q)
    return result.scalars().all()

@router.post("/records/", response_model=GivingRecordOut, status_code=201)
async def create_giving_record(data: GivingRecordCreate, db: AsyncSession = Depends(get_db)):
    record = GivingRecord(**data.model_dump())
    db.add(record)
    await db.flush()
    cat_result = await db.execute(select(GivingCategory).where(GivingCategory.id == data.category_id))
    cat = cat_result.scalar_one_or_none()
    if cat:
        method_prefix = "mpesa" if data.payment_method == "mpesa" else "cash"
        debit = "1010" if data.payment_method == "mpesa" else "1000"
        await post_gl(
            db=db,
            church_id=data.church_id,
            branch_id=data.branch_id,
            debit_code=debit,
            credit_code=cat.gl_credit_code,
            amount=data.amount_kes,
            description=f"{cat.name} received - {method_prefix}",
            event_type="giving_received",
            idempotency_key=f"giving:{record.id}",
        )
    await db.commit()
    await db.refresh(record)
    member_name = None
    if record.member_id:
        m = await db.get(Member, record.member_id)
        if m:
            member_name = f"{m.first_name} {m.last_name}"
    return {
        **data.model_dump(),
        "id": record.id,
        "created_at": record.created_at,
        "member_name": member_name,
        "category_name": cat.name if cat else None,
    }

@router.get("/records/", response_model=List[GivingRecordOut])
async def list_giving_records(
    church_id: str = None,
    branch_id: str = None,
    member_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    q = select(GivingRecord).options(
        selectinload(GivingRecord.member),
        selectinload(GivingRecord.category)
    ).where(GivingRecord.is_deleted == False)
    if church_id:
        q = q.where(GivingRecord.church_id == church_id)
    if branch_id:
        q = q.where(GivingRecord.branch_id == branch_id)
    if member_id:
        q = q.where(GivingRecord.member_id == member_id)
    q = q.order_by(GivingRecord.created_at.desc())
    result = await db.execute(q)
    records = result.scalars().all()
    out = []
    for r in records:
        out.append({
            "id": r.id, "church_id": r.church_id, "branch_id": r.branch_id,
            "member_id": r.member_id, "session_id": r.session_id,
            "category_id": r.category_id, "amount_kes": r.amount_kes,
            "payment_method": r.payment_method, "mpesa_ref": r.mpesa_ref,
            "envelope_number": r.envelope_number, "notes": r.notes,
            "created_at": r.created_at,
            "member_name": f"{r.member.first_name} {r.member.last_name}" if r.member else None,
            "category_name": r.category.name if r.category else None,
        })
    return out

@router.get("/summary/")
async def giving_summary(church_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GivingCategory.name, func.sum(GivingRecord.amount_kes).label("total"))
        .join(GivingRecord, GivingRecord.category_id == GivingCategory.id)
        .where(GivingRecord.church_id == church_id)
        .group_by(GivingCategory.name)
    )
    rows = result.all()
    return [{"category": r.name, "total_kes": r.total or 0} for r in rows]
