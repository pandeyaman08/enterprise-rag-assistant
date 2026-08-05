from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

# The Engine: one per application lifetime. Manages the underlying
# connection pool to PostgreSQL. echo=settings.DEBUG logs every SQL
# statement to the console — useful in development, must be off in prod
# since it leaks query details and hurts performance.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# The Session factory: creates new AsyncSession objects on demand.
# expire_on_commit=False keeps loaded objects usable after commit,
# which avoids extra queries when returning data in API responses.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency-injected database session for FastAPI routes.

    Yields a session scoped to a single request, and guarantees it is
    closed afterward — even if the request raises an exception. This
    pattern (yield inside a try/finally) is what makes it usable with
    FastAPI's `Depends()` system.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
