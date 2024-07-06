from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.settings import settings

db_url = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}"
engine_test = create_async_engine(
    db_url,
    echo=True,
    future=True,
)
new_session = async_sessionmaker(
    engine_test,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_session() -> AsyncSession:
    async with new_session() as session:
        yield session
