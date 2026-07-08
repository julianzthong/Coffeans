import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_list_beans_returns_only_active_items(client: AsyncClient, create_roastery, create_bean, db_session: AsyncSession):
    roastery = await create_roastery(name="Bean Roastery")
    await create_bean(roastery_id=str(roastery.id), name="Active Bean")

    inactive = await create_bean(roastery_id=str(roastery.id), name="Inactive Bean")
    inactive.is_active = False
    db_session.add(inactive)
    await db_session.commit()

    response = await client.get("/api/beans")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["name"] == "Active Bean"


@pytest.mark.asyncio
async def test_get_bean_returns_404_for_missing_id(client: AsyncClient):
    response = await client.get(f"/api/beans/{uuid.uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Bean not found"


@pytest.mark.asyncio
async def test_create_bean_persists_new_record(client: AsyncClient, create_roastery):
    roastery = await create_roastery(name="Create Roastery")

    response = await client.post(
        "/api/beans",
        json={
            "roastery_id": str(roastery.id),
            "name": "New Bean",
            "origin_country": "Ethiopia",
            "processing_method": "washed",
            "roast_level": "medium",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["name"] == "New Bean"
    assert payload["origin_country"] == "Ethiopia"
