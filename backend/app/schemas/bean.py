import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.bean import ProcessingMethod, RoastLevel


class BeanCreate(BaseModel):
    roastery_id: uuid.UUID
    name: str
    origin_country: Optional[str] = None
    origin_region: Optional[str] = None
    processing_method: Optional[ProcessingMethod] = None
    roast_level: Optional[RoastLevel] = None
    tasting_notes_raw: Optional[str] = None


class BeanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    roastery_id: uuid.UUID
    name: str
    origin_country: Optional[str]
    origin_region: Optional[str]
    processing_method: Optional[ProcessingMethod]
    roast_level: Optional[RoastLevel]
    tasting_notes_raw: Optional[str]
    tasting_notes_structured: dict
    is_active: bool
