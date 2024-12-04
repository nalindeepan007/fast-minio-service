
import os
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.dbModel import Base



tmpPostgres = urlparse(os.getenv("DATABASE_URL"))


engine = create_async_engine(f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require", echo=True)



async def createDbSchema() -> None:
    """ create the initial db schema for neon db postgres"""
    async with engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all) # droping existing
            await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    



AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Dependency to use in FastAPI for database sessions
async def getDb():
    """to fetch DB sessions"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
            # also gracefully close karna he !!!! (always remember)

async def shutdownDatabase():
    """Properly close database engine"""
    await engine.dispose()



