import os
from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://coffeans:coffeans@db_test:5432/coffeans_test",
)

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.bean import Bean
from app.models.roastery import Roastery
from app.models.user import User

engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """Create all tables once per test session, drop them at the end."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """One connection + outer transaction per test; rolled back after, so tests never leak state."""
    async with engine.connect() as conn:
        trans = await conn.begin()
        session = TestSessionLocal(bind=conn)
        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()


@pytest_asyncio.fixture()
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def create_user(db_session: AsyncSession):
    async def _create_user(
        email: str = "user@example.com",
        password: str = "secret123",
        display_name: str = "Test User",
    ) -> User:
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
    async def _create_bean(roastery: Roastery, name: str = "Test Bean") -> Bean:
        # Requires a real Roastery fixture — no fabricated UUIDs, so FK integrity
        # is actually exercised the way it would be against production Postgres.
        bean = Bean(roastery_id=roastery.id, name=name)
        db_session.add(bean)
        await db_session.commit()
        await db_session.refresh(bean)
        return bean

    return _create_bean