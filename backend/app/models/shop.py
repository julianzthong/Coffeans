import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roastery_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roasteries.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(500))
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    google_place_id: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    amenities: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    roastery: Mapped["Roastery"] = relationship(back_populates="shops")
    beans: Mapped[list["Bean"]] = relationship(secondary="shop_beans", back_populates="shops")


class ShopBean(Base):
    __tablename__ = "shop_beans"

    shop_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("shops.id"), primary_key=True)
    bean_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("beans.id"), primary_key=True)
    available_since: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
