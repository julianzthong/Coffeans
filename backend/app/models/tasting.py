import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BrewMethod(str, enum.Enum):
    pour_over = "pour_over"
    espresso = "espresso"
    french_press = "french_press"
    aeropress = "aeropress"
    drip = "drip"
    cold_brew = "cold_brew"
    other = "other"


class TastingEntry(Base):
    __tablename__ = "tasting_entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    bean_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("beans.id"))
    rating: Mapped[int | None] = mapped_column(Integer)  # 1-5
    notes_raw: Mapped[str | None] = mapped_column(Text)
    notes_structured: Mapped[dict] = mapped_column(JSONB, default=dict)
    brew_method: Mapped[BrewMethod | None] = mapped_column(Enum(BrewMethod))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="tasting_entries")
    bean: Mapped["Bean"] = relationship(back_populates="tasting_entries")
