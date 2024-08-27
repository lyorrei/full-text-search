from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/mydb"

database = Database(DATABASE_URL)

# Create async SQLAlchemy engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Dependency to get the async DB session
async def get_db():
    async with async_session() as session:
        yield session