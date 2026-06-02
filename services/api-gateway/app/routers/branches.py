from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.church import Branch
from app.schemas.church import BranchCreate, BranchOut
from typing import List

router = APIRouter()

@router.post("/", response_model=BranchOut, status_code=201)
async def create_branch(data: BranchCreate, db: AsyncSession = Depends(get_db)):
    branch = Branch(**data.model_dump())
    db.add(branch)
    await db.commit()
    await db.refresh(branch)
    return branch

@router.get("/", response_model=List[BranchOut])
async def list_branches(church_id: str = None, db: AsyncSession = Depends(get_db)):
    q = select(Branch).where(Branch.is_deleted == False)
    if church_id:
        q = q.where(Branch.church_id == church_id)
    result = await db.execute(q)
    return result.scalars().all()

@router.get("/{branch_id}", response_model=BranchOut)
async def get_branch(branch_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    branch = result.scalar_one_or_none()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch
