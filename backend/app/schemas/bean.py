import uuid

from pydantic import BaseModel

from app.models.bean import ProcessingMethod, RoastLevel


class BeanCreate(BaseModel):
    roastery_id: uuid.UUID
    name: str
    origin_country: str | None = None
    origin_region: str | None = None
    processing_method: ProcessingMethod | None = None
    roast_level: RoastLevel | None = None
    tasting_notes_raw: str | None = None


class BeanOut(BaseModel):
    id: uuid.UUID
    roastery_id: uuid.UUID
    name: str
    origin_country: str | None
    origin_region: str | None
    processing_method: ProcessingMethod | None
    roast_level: RoastLevel | None
    tasting_notes_raw: str | None
    tasting_notes_structured: dict
    is_active: bool

    class Config:
        from_attributes = True
