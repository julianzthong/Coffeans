import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.roastery import DataSource


class RoasteryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    has_storefront: bool = False


class RoasteryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: Optional[str]
    website: Optional[str]
    city: Optional[str]
    state: Optional[str]
    has_storefront: bool
    source: DataSource


class ShopCreate(BaseModel):
    roastery_id: Optional[uuid.UUID] = None
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    amenities: dict = {}


class ShopOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    roastery_id: Optional[uuid.UUID]
    name: str
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    amenities: dict
