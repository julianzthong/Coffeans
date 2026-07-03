import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.bean import Bean
from app.schemas.bean import BeanCreate, BeanOut
from app.services.claude_service import parse_flavor_notes

router = APIRouter(prefix="/api/beans", tags=["beans"])


@router.get("", response_model=list[BeanOut])
async def list_beans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bean).where(Bean.is_active.is_(True)).order_by(Bean.name))
    return result.scalars().all()


@router.get("/{bean_id}", response_model=BeanOut)
async def get_bean(bean_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    bean = await db.get(Bean, bean_id)
    if not bean:
        raise HTTPException(status_code=404, detail="Bean not found")
    return bean


@router.post("", response_model=BeanOut, status_code=201)
async def create_bean(payload: BeanCreate, db: AsyncSession = Depends(get_db)):
    bean = Bean(**payload.model_dump())

    # If raw tasting notes were provided, ask Claude to structure them into tags.
    if bean.tasting_notes_raw:
        bean.tasting_notes_structured = await parse_flavor_notes(bean.tasting_notes_raw)

    db.add(bean)
    await db.commit()
    await db.refresh(bean)
    return bean
