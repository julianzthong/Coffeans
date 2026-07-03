"""Quick seed script for local dev. Run with: python -m app.db.seed"""
import asyncio

from app.db.session import AsyncSessionLocal
from app.models.bean import Bean, ProcessingMethod, RoastLevel
from app.models.roastery import Roastery
from app.models.shop import Shop, ShopBean


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        roastery = Roastery(
            name="Ember & Origin",
            description="Small-batch roaster focused on washed Ethiopian and Colombian lots.",
            city="San Francisco",
            state="CA",
            has_storefront=True,
        )
        db.add(roastery)
        await db.flush()

        shop = Shop(
            roastery_id=roastery.id,
            name="Ember & Origin — Valencia St",
            address="123 Valencia St, San Francisco, CA",
            latitude=37.7599,
            longitude=-122.4212,
            amenities={"laptop_friendly": True, "oat_milk": True, "seating": True},
        )
        db.add(shop)

        bean = Bean(
            roastery_id=roastery.id,
            name="Yirgacheffe Konga",
            origin_country="Ethiopia",
            origin_region="Yirgacheffe",
            processing_method=ProcessingMethod.washed,
            roast_level=RoastLevel.light,
            tasting_notes_raw="Bright and floral, like jasmine tea with a squeeze of lemon. Light body, very clean finish.",
            tasting_notes_structured={
                "flavor_tags": ["jasmine", "lemon", "black tea"],
                "acidity": "high",
                "body": "light",
                "sweetness": "medium",
                "summary": "Floral and citrusy with a clean, tea-like finish.",
            },
        )
        db.add(bean)
        await db.flush()

        db.add(ShopBean(shop_id=shop.id, bean_id=bean.id))
        await db.commit()

    print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(seed())
