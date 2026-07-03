import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.shop import Shop
from app.schemas.shop import ShopCreate, ShopOut

router = APIRouter(prefix="/api/shops", tags=["shops"])


@router.get("", response_model=list[ShopOut])
async def list_shops(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Shop).order_by(Shop.name))
    return result.scalars().all()


@router.get("/{shop_id}", response_model=ShopOut)
async def get_shop(shop_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    shop = await db.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return shop


@router.post("", response_model=ShopOut, status_code=201)
async def create_shop(payload: ShopCreate, db: AsyncSession = Depends(get_db)):
    shop = Shop(**payload.model_dump())
    db.add(shop)
    await db.commit()
    await db.refresh(shop)
    return shop
