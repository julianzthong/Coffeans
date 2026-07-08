import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.tasting import BrewMethod


class TastingEntryCreate(BaseModel):
    bean_id: uuid.UUID
    rating: Optional[int] = None
    notes_raw: Optional[str] = None
    brew_method: Optional[BrewMethod] = None


class TastingEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    bean_id: uuid.UUID
    rating: Optional[int]
    notes_raw: Optional[str]
    notes_structured: dict
    brew_method: Optional[BrewMethod]
    created_at: datetime
