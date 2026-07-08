import os
import uuid
from collections.abc import AsyncGenerator
from typing import Optional

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.dialects.sqlite.base import SQLiteTypeCompiler
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.bean import Bean
from app.models.roastery import Roastery
from app.models.user import User


if not hasattr(SQLiteTypeCompiler, "visit_JSONB"):
    SQLiteTypeCompiler.visit_JSONB = SQLiteTypeCompiler.visit_JSON

if not hasattr(SQLiteTypeCompiler, "visit_UUID"):
    SQLiteTypeCompiler.visit_UUID = lambda self, type_, **kw: self.visit_STRING(type_, **kw)


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture()
async def client(db_session: AsyncSession):
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def create_user(db_session: AsyncSession):
    async def _create_user(email: str = "user@example.com", password: str = "secret123", display_name: str = "Test User") -> User:
        from app.core.security import hash_password

        user = User(email=email, hashed_password=hash_password(password), display_name=display_name)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    return _create_user


@pytest_asyncio.fixture()
async def create_roastery(db_session: AsyncSession):
    async def _create_roastery(name: str = "Test Roastery") -> Roastery:
        roastery = Roastery(name=name)
        db_session.add(roastery)
        await db_session.commit()
        await db_session.refresh(roastery)
        return roastery

    return _create_roastery


@pytest_asyncio.fixture()
async def create_bean(db_session: AsyncSession):
    async def _create_bean(roastery_id: Optional[str] = None, name: str = "Test Bean") -> Bean:
        bean = Bean(
            roastery_id=uuid.UUID(roastery_id) if roastery_id else uuid.uuid4(),
            name=name,
        )
        db_session.add(bean)
        await db_session.commit()
        await db_session.refresh(bean)
        return bean

    return _create_bean
