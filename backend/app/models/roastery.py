import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DataSource(str, enum.Enum):
    manual = "manual"
    google_places = "google_places"
    scraped = "scraped"


class Roastery(Base):
    __tablename__ = "roasteries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000))
    website: Mapped[str | None] = mapped_column(String(500))
    city: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    has_storefront: Mapped[bool] = mapped_column(Boolean, default=False)
    source: Mapped[DataSource] = mapped_column(Enum(DataSource), default=DataSource.manual)
    external_id: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    beans: Mapped[list["Bean"]] = relationship(back_populates="roastery")
    shops: Mapped[list["Shop"]] = relationship(back_populates="roastery")
