from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.church import AttendanceSession, Branch
from app.schemas.church import AttendanceCreate, AttendanceOut
from typing import List, Optional

router = APIRouter()

@router.post("/sessions/", response_model=AttendanceOut, status_code=201)
async def create_session(data: AttendanceCreate, db: AsyncSession = Depends(get_db)):
    session = AttendanceSession(**data.model_dump())
    db.add(session)
    await db.commit()
    await db.refresh(session)
    branch_name = None
    if session.branch_id:
        br = await db.get(Branch, session.branch_id)
        branch_name = br.name if br else None
    result = AttendanceOut.model_validate(session)
    result.branch_name = branch_name
    return result

@router.get("/sessions/", response_model=List[AttendanceOut])
async def list_sessions(
    church_id: str = None,
    branch_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    q = select(AttendanceSession).options(selectinload(AttendanceSession.branch)).where(AttendanceSession.is_deleted == False)
    if church_id:
        q = q.where(AttendanceSession.church_id == church_id)
    if branch_id:
        q = q.where(AttendanceSession.branch_id == branch_id)
    q = q.order_by(AttendanceSession.session_date.desc())
    result = await db.execute(q)
    sessions = result.scalars().all()
    out = []
    for s in sessions:
        d = AttendanceOut.model_validate(s)
        d.branch_name = s.branch.name if s.branch else None
        out.append(d)
    return out

@router.get("/sessions/{session_id}", response_model=AttendanceOut)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AttendanceSession)
        .options(selectinload(AttendanceSession.branch))
        .where(AttendanceSession.id == session_id)
    )
    s = result.scalar_one_or_none()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    d = AttendanceOut.model_validate(s)
    d.branch_name = s.branch.name if s.branch else None
    return d
