cat > entrypoint.sh << 'EOF'
#!/bin/sh
set -e

echo "Waiting for database to accept connections..."
until python -c "
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

async def check():
    engine = create_async_engine(settings.database_url)
    try:
        async with engine.connect() as conn:
            pass
    finally:
        await engine.dispose()

asyncio.run(check())
" 2>/dev/null; do
  sleep 1
done
echo "Database is up."

echo "Applying database migrations..."
alembic upgrade head

echo "Starting API server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
EOF

chmod +x entrypoint.sh