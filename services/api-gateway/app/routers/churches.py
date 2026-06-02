from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.church import Church
from app.schemas.church import ChurchCreate, ChurchOut
from typing import List

router = APIRouter()

@router.post("/", response_model=ChurchOut, status_code=201)
async def create_church(data: ChurchCreate, db: AsyncSession = Depends(get_db)):
    church = Church(**data.model_dump())
    db.add(church)
    await db.commit()
    await db.refresh(church)
    return church

@router.get("/", response_model=List[ChurchOut])
async def list_churches(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Church).where(Church.is_deleted == False))
    return result.scalars().all()

@router.get("/{church_id}", response_model=ChurchOut)
async def get_church(church_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Church).where(Church.id == church_id))
    church = result.scalar_one_or_none()
    if not church:
        raise HTTPException(status_code=404, detail="Church not found")
    return church
