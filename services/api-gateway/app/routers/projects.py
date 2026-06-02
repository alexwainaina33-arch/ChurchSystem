from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.church import Project
from app.schemas.church import ProjectCreate, ProjectOut
from typing import List

router = APIRouter()

@router.post("/", response_model=ProjectOut, status_code=201)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project = Project(**data.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    result = ProjectOut.model_validate(project)
    result.progress_percent = round((project.collected_amount_kes / project.target_amount_kes * 100), 1) if project.target_amount_kes > 0 else 0
    return result

@router.get("/", response_model=List[ProjectOut])
async def list_projects(church_id: str = None, db: AsyncSession = Depends(get_db)):
    q = select(Project).where(Project.is_deleted == False)
    if church_id:
        q = q.where(Project.church_id == church_id)
    q = q.order_by(Project.created_at.desc())
    result = await db.execute(q)
    projects = result.scalars().all()
    out = []
    for p in projects:
        d = ProjectOut.model_validate(p)
        d.progress_percent = round((p.collected_amount_kes / p.target_amount_kes * 100), 1) if p.target_amount_kes > 0 else 0
        out.append(d)
    return out

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.id == project_id))
    p = result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    d = ProjectOut.model_validate(p)
    d.progress_percent = round((p.collected_amount_kes / p.target_amount_kes * 100), 1) if p.target_amount_kes > 0 else 0
    return d
