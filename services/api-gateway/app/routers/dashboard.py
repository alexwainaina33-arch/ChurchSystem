from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.church import Branch, Member, GivingRecord, AttendanceSession, Project, Transaction, Account
from typing import List
from datetime import date

router = APIRouter()

@router.get("/hq/")
async def hq_dashboard(church_id: str, db: AsyncSession = Depends(get_db)):
    total_members = await db.execute(select(func.count(Member.id)).where(Member.church_id == church_id, Member.is_deleted == False))
    total_giving = await db.execute(select(func.sum(GivingRecord.amount_kes)).where(GivingRecord.church_id == church_id))
    total_projects = await db.execute(select(func.count(Project.id)).where(Project.church_id == church_id, Project.status == "active"))
    branches_result = await db.execute(select(Branch).where(Branch.church_id == church_id, Branch.is_deleted == False))
    branches = branches_result.scalars().all()
    branch_cards = []
    for b in branches:
        bm = await db.execute(select(func.count(Member.id)).where(Member.branch_id == b.id))
        bg = await db.execute(select(func.sum(GivingRecord.amount_kes)).where(GivingRecord.branch_id == b.id))
        branch_cards.append({
            "branch_id": str(b.id),
            "branch_name": b.name,
            "pastor": b.pastor_name,
            "total_members": bm.scalar() or 0,
            "total_giving_kes": bg.scalar() or 0,
        })
    return {
        "total_members": total_members.scalar() or 0,
        "total_giving_kes": total_giving.scalar() or 0,
        "active_projects": total_projects.scalar() or 0,
        "total_branches": len(branches),
        "branches": branch_cards,
    }

@router.get("/finance/")
async def finance_dashboard(church_id: str, db: AsyncSession = Depends(get_db)):
    accounts_result = await db.execute(
        select(Account).where(Account.church_id == church_id, Account.is_deleted == False).order_by(Account.code)
    )
    accounts = accounts_result.scalars().all()
    txns_result = await db.execute(
        select(Transaction).where(Transaction.church_id == church_id).order_by(Transaction.created_at.desc()).limit(20)
    )
    txns = txns_result.scalars().all()
    return {
        "accounts": [{"code": a.code, "name": a.name, "type": a.type, "balance_kes": a.balance} for a in accounts],
        "recent_transactions": [
            {"date": str(t.created_at), "debit": t.debit_account_code, "credit": t.credit_account_code,
             "amount_kes": t.amount, "description": t.description, "event_type": t.event_type}
            for t in txns
        ],
    }
