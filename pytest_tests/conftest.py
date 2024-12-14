from typing import AsyncGenerator

import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.db import Model, get_db
from app.models import Item, User, UserPurchase
from app.routers import (gen_recommendation_router, item_router,
                         purchase_router, recommendation_router, user_router)

app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)
app.include_router(purchase_router)
app.include_router(recommendation_router)
app.include_router(gen_recommendation_router)

engine_test = create_async_engine(
    'sqlite+aiosqlite:///test_db.db',
)


test_db_session = async_sessionmaker(engine_test, expire_on_commit=False)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    '''Переопределяет сессию бд.'''
    async with test_db_session() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

USERNAME1 = 'Kate'
USERNAME2 = 'Pasha'
USERNAME3 = 'Masha'

ITEM_NAME1 = 'white ball'
ITEM_NAME2 = 'black ball'
ITEM_NAME3 = 'green ball'
ITEM_NAME4 = 'carrot chips'
ITEM_NAME5 = 'chips'
CATEGORY1 = 'balls'
CATEGORY2 = 'chips'


@pytest_asyncio.fixture(scope='function')
async def test_db():
    '''
    Запускает тестовую базу данных и после каждого теста удаляет её.
    '''
    async with engine_test.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield test_db_session()
    async with engine_test.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


@pytest_asyncio.fixture(scope='function')
async def async_db(test_db):
    '''Сессия тестовой базы данных.'''

    async with test_db_session() as session:
        await session.begin()

        yield session

        await session.rollback()


@pytest_asyncio.fixture(scope='function')
async def client():
    '''Фикстура клиента.'''
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url='http://test') as client:
        yield client


@pytest_asyncio.fixture(scope='function')
async def item1(async_db: AsyncSession) -> Item:
    '''Фикстура товара 1.'''
    item = Item(name=ITEM_NAME1,
                category=CATEGORY1)
    async_db.add(item)
    await async_db.commit()
    await async_db.refresh(item)
    return item


@pytest_asyncio.fixture(scope='function')
async def item2(async_db: AsyncSession) -> Item:
    '''Фикстура товара 2.'''
    item = Item(name=ITEM_NAME2,
                category=CATEGORY1)
    async_db.add(item)
    await async_db.commit()
    await async_db.refresh(item)
    return item


@pytest_asyncio.fixture(scope='function')
async def item3(async_db: AsyncSession) -> Item:
    '''Фикстура товара 3.'''
    item = Item(name=ITEM_NAME3,
                category=CATEGORY1)
    async_db.add(item)
    await async_db.commit()
    await async_db.refresh(item)
    return item


@pytest_asyncio.fixture(scope='function')
async def item4(async_db: AsyncSession) -> Item:
    '''Фикстура товара 4.'''
    item = Item(name=ITEM_NAME4,
                category=CATEGORY2)
    async_db.add(item)
    await async_db.commit()
    await async_db.refresh(item)
    return item


@pytest_asyncio.fixture(scope='function')
async def item5(async_db: AsyncSession) -> Item:
    '''Фикстура товара 5.'''
    item = Item(name=ITEM_NAME5,
                category=CATEGORY2)
    async_db.add(item)
    await async_db.commit()
    await async_db.refresh(item)
    return item


@pytest_asyncio.fixture(scope='function')
async def user1(async_db: AsyncSession) -> User:
    '''Фикстура пользователя 1.'''
    user = User(username=USERNAME1)
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    return user


@pytest_asyncio.fixture(scope='function')
async def user2(async_db: AsyncSession) -> User:
    '''Фикстура пользователя 2.'''
    user = User(username=USERNAME2)
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    return user


@pytest_asyncio.fixture(scope='function')
async def user3(async_db: AsyncSession) -> User:
    '''Фикстура пользователя 3.'''
    user = User(username=USERNAME3)
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    return user


@pytest_asyncio.fixture(scope='function')
async def purchase1_user1(async_db: AsyncSession, user1: User,
                          item1: Item) -> UserPurchase:
    '''Фикстура покупки пользователя 1.'''

    purchase = UserPurchase(user_id=user1.id,
                            item_id=item1.id,
                            category=item1.category)
    async_db.add(purchase)
    await async_db.commit()
    return purchase


@pytest_asyncio.fixture(scope='function')
async def purchase2_user1(async_db: AsyncSession, user1: User,
                          item2: Item) -> UserPurchase:
    '''Фикстура покупки пользователя 1.'''

    purchase = UserPurchase(user_id=user1.id,
                            item_id=item2.id,
                            category=item2.category)
    async_db.add(purchase)
    await async_db.commit()
    return purchase


@pytest_asyncio.fixture(scope='function')
async def purchase1_user2(async_db: AsyncSession, user2: User,
                          item2: Item) -> UserPurchase:
    '''Фикстура покупки пользователя 2.'''

    purchase = UserPurchase(user_id=user2.id,
                            item_id=item2.id,
                            category=item2.category)
    async_db.add(purchase)
    await async_db.commit()
    return purchase


@pytest_asyncio.fixture(scope='function')
async def purchase2_user2(async_db: AsyncSession, user2: User,
                          item3: Item) -> UserPurchase:
    '''Фикстура покупки пользователя 2.'''

    purchase = UserPurchase(user_id=user2.id,
                            item_id=item3.id,
                            category=item3.category)
    async_db.add(purchase)
    await async_db.commit()
    return purchase


@pytest_asyncio.fixture(scope='function')
async def purchase3_user2(async_db: AsyncSession, user2: User,
                          item5: Item) -> UserPurchase:
    '''Фикстура покупки пользователя 2.'''

    purchase = UserPurchase(user_id=user2.id,
                            item_id=item5.id,
                            category=item5.category)
    async_db.add(purchase)
    await async_db.commit()
    return purchase


@pytest_asyncio.fixture(scope='function')
async def purchase1_user3(async_db: AsyncSession, user3: User,
                          item4: Item) -> UserPurchase:
    '''Фикстура покупки пользователя 3.'''

    purchase = UserPurchase(user_id=user3.id,
                            item_id=item4.id,
                            category=item4.category)
    async_db.add(purchase)
    await async_db.commit()
    return purchase
