import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ProcessingMethod(str, enum.Enum):
    washed = "washed"
    natural = "natural"
    honey = "honey"
    anaerobic = "anaerobic"
    other = "other"


class RoastLevel(str, enum.Enum):
    light = "light"
    medium = "medium"
    dark = "dark"


class Bean(Base):
    __tablename__ = "beans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roastery_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("roasteries.id"))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    origin_country: Mapped[Optional[str]] = mapped_column(String(100))
    origin_region: Mapped[Optional[str]] = mapped_column(String(100))
    processing_method: Mapped[Optional[ProcessingMethod]] = mapped_column(Enum(ProcessingMethod))
    roast_level: Mapped[Optional[RoastLevel]] = mapped_column(Enum(RoastLevel))
    tasting_notes_raw: Mapped[Optional[str]] = mapped_column(Text)
    tasting_notes_structured: Mapped[dict] = mapped_column(JSONB, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    roastery: Mapped["Roastery"] = relationship(back_populates="beans")
    shops: Mapped[list["Shop"]] = relationship(secondary="shop_beans", back_populates="beans")
    tasting_entries: Mapped[list["TastingEntry"]] = relationship(back_populates="bean")
