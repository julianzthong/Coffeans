from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, beans, roasteries, shops, tasting
from app.core.config import settings

app = FastAPI(title="Coffeans API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(roasteries.router)
app.include_router(shops.router)
app.include_router(beans.router)
app.include_router(tasting.router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
