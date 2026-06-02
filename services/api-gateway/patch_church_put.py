import os
router_file = '/app/app/routers/churches.py'
content = open(router_file).read()
if 'put' not in content:
    content += """
@router.put("/{church_id}", response_model=ChurchOut)
async def update_church(church_id: str, data: ChurchCreate, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(Church).where(Church.id == church_id))
    church = result.scalar_one_or_none()
    if not church:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Church not found")
    for k, v in data.model_dump().items():
        setattr(church, k, v)
    await db.commit()
    await db.refresh(church)
    return church
"""
    open(router_file, 'w').write(content)
    print('PUT endpoint added')
else:
    print('Already exists')
