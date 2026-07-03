import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.roastery import Roastery
from app.schemas.shop import RoasteryCreate, RoasteryOut

router = APIRouter(prefix="/api/roasteries", tags=["roasteries"])


@router.get("", response_model=list[RoasteryOut])
async def list_roasteries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Roastery).order_by(Roastery.name))
    return result.scalars().all()


@router.get("/{roastery_id}", response_model=RoasteryOut)
async def get_roastery(roastery_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    roastery = await db.get(Roastery, roastery_id)
    if not roastery:
        raise HTTPException(status_code=404, detail="Roastery not found")
    return roastery


@router.post("", response_model=RoasteryOut, status_code=201)
async def create_roastery(payload: RoasteryCreate, db: AsyncSession = Depends(get_db)):
    roastery = Roastery(**payload.model_dump())
    db.add(roastery)
    await db.commit()
    await db.refresh(roastery)
    return roastery
