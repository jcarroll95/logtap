from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession


# 1. Define your connection string
# Format: postgresql+asyncpg://user:password@host:port/dbname
# must use +asynchpg for async ops, or it will default to psycopg and fail, this is DRIVER PREFIX
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/logtap"

# 2. Create the Async Engine - this is the CONNECTION POOL
# 'echo=True' is great for development as it logs all SQL queries
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. Create the SessionLocal factory - this generates individual sessions
# expire_on_commit=False is important for async to prevent unintended IO
# when accessing attributes after a commit.
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False      # needed for async behavior so lazy loading errors don't happen
)

# 4. Create a Base class for your SQLAlchemy models
class Base(DeclarativeBase):
    pass

# 5. create a generator function and inject it into the routes using Depends
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
    # The 'async with' block ensures the session is CLOSED
    # automatically after the route finishes, even if an error occurs.