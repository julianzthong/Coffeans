import uuid

from pydantic import BaseModel

from app.models.roastery import DataSource


class RoasteryCreate(BaseModel):
    name: str
    description: str | None = None
    website: str | None = None
    city: str | None = None
    state: str | None = None
    has_storefront: bool = False


class RoasteryOut(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    website: str | None
    city: str | None
    state: str | None
    has_storefront: bool
    source: DataSource

    class Config:
        from_attributes = True


class ShopCreate(BaseModel):
    roastery_id: uuid.UUID | None = None
    name: str
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    amenities: dict = {}


class ShopOut(BaseModel):
    id: uuid.UUID
    roastery_id: uuid.UUID | None
    name: str
    address: str | None
    latitude: float | None
    longitude: float | None
    amenities: dict

    class Config:
        from_attributes = True
