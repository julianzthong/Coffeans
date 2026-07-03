import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.tasting import TastingEntry
from app.models.user import User
from app.schemas.tasting import TastingEntryCreate, TastingEntryOut
from app.services.claude_service import parse_flavor_notes

router = APIRouter(prefix="/api/tasting-entries", tags=["tasting"])


@router.get("", response_model=list[TastingEntryOut])
async def list_my_tasting_entries(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(TastingEntry)
        .where(TastingEntry.user_id == current_user.id)
        .order_by(TastingEntry.created_at.desc())
    )
    return result.scalars().all()


@router.post("", response_model=TastingEntryOut, status_code=201)
async def create_tasting_entry(
    payload: TastingEntryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = TastingEntry(**payload.model_dump(), user_id=current_user.id)

    if entry.notes_raw:
        entry.notes_structured = await parse_flavor_notes(entry.notes_raw)

    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=204)
async def delete_tasting_entry(
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = await db.get(TastingEntry, entry_id)
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tasting entry not found")
    await db.delete(entry)
    await db.commit()
