from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.church import Message
from app.schemas.church import MessageCreate, MessageOut
from typing import List

router = APIRouter()

@router.post("/", response_model=MessageOut, status_code=201)
async def send_message(data: MessageCreate, db: AsyncSession = Depends(get_db)):
    msg = Message(**data.model_dump())
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

@router.get("/", response_model=List[MessageOut])
async def list_messages(church_id: str = None, db: AsyncSession = Depends(get_db)):
    q = select(Message).where(Message.is_deleted == False)
    if church_id:
        q = q.where(Message.church_id == church_id)
    q = q.order_by(Message.created_at.desc())
    result = await db.execute(q)
    return result.scalars().all()
