import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from app.models import Model
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

engine = create_async_engine(
    f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@postgres/{DB_NAME}'
)

db_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with db_session() as session:
        try:
            yield session
        finally:
            await session.close()
