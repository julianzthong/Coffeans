import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.tasting import BrewMethod


class TastingEntryCreate(BaseModel):
    bean_id: uuid.UUID
    rating: int | None = None
    notes_raw: str | None = None
    brew_method: BrewMethod | None = None


class TastingEntryOut(BaseModel):
    id: uuid.UUID
    bean_id: uuid.UUID
    rating: int | None
    notes_raw: str | None
    notes_structured: dict
    brew_method: BrewMethod | None
    created_at: datetime

    class Config:
        from_attributes = True
