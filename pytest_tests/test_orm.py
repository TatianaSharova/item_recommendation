from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .conftest import CATEGORY1, ITEM_NAME1
from app.models import Item, Recommendation, User, UserPurchase


@pytest.mark.asyncio
async def test_add_user(client: AsyncClient, async_db: AsyncSession):
    '''Проверка на создание пользователя.'''
    data = {'username': 'Moa'}

    response = await client.post('/users', json=data)

    response_data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert response_data['status'] == 'Пользователь создан.'


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient, async_db: AsyncSession,
                         user1: User, user2: User, user3: User) -> None:
    '''Проверка на получение всех пользователей.'''
    response = await client.get('/users')
    response_data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response_data['data'], list)
    assert len(response_data['data']) == 3


@pytest.mark.asyncio
async def test_add_item(client: AsyncClient, async_db: AsyncSession):
    '''Проверка на создание товара.'''
    data = {'name': ITEM_NAME1,
            'category': CATEGORY1}

    response = await client.post('/items', json=data)

    response_data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert response_data['data']['name'] == ITEM_NAME1
    assert response_data['data']['category'] == CATEGORY1


@pytest.mark.asyncio
async def test_get_item_by_id(client: AsyncClient, async_db: AsyncSession,
                              item1: Item) -> None:
    '''Проверка на получение товара по id.'''
    response = await client.get(f'/items/{item1.id}')
    response_data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_data['data']['id'] == str(item1.id)


@pytest.mark.asyncio
async def test_get_items(client: AsyncClient, async_db: AsyncSession,
                         item1: Item, item2: Item, item3: Item) -> None:
    '''Проверка на получение списка товаров.'''
    response = await client.get('/items')
    response_data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response_data['data'], list)
    assert len(response_data['data']) == 3


@pytest.mark.asyncio
async def test_add_purchase(client: AsyncClient, async_db: AsyncSession,
                            user1: User, item1: Item, item2: Item):
    '''Проверка на создание покупки.'''
    data = {
        'user_id': str(user1.id),
        'cart': [
            {'id': str(item1.id), 'category': item1.category},
            {'id': str(item2.id), 'category': item2.category}
        ]
    }

    response = await client.post('/purchases', json=data)

    response_data = response.json()

    query = select(UserPurchase).where(UserPurchase.user_id == user1.id)
    result = await async_db.execute(query)
    purchases = result.scalars().all()
    assert len(purchases) == 2
    assert response.status_code == HTTPStatus.CREATED
    assert response_data['status'] == (
        f'Покупка для пользователя {user1.id} успешно добавлена.')


@pytest.mark.asyncio
async def test_get_purchases(client: AsyncClient, async_db: AsyncSession,
                             user1: User, item1: Item, item2: Item,
                             purchase1_user1: UserPurchase,
                             purchase2_user1: UserPurchase) -> None:
    '''Проверка на получение списка покупок.'''
    response = await client.get('/purchases')
    response_data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response_data['data'], list)
    assert len(response_data['data']) == 2


@pytest.mark.asyncio
async def test_get_user_purchases(
    client: AsyncClient, async_db: AsyncSession,
    user1: User, item1: Item, item2: Item,
    purchase1_user1: UserPurchase,
    purchase2_user1: UserPurchase
) -> None:
    '''Проверка на получение списка покупок пользователя.'''
    response = await client.get(f'/purchases?user_id={user1.id}')
    response_data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response_data['data'], list)
    assert len(response_data['data']) == 2


@pytest.mark.asyncio
async def test_start_generation(
    client: AsyncClient, async_db: AsyncSession,
    user1: User, user2: User, user3: User,
    item1: Item, item2: Item, item3: Item, item4: Item, item5: Item,
    purchase1_user1: UserPurchase, purchase2_user1: UserPurchase,
    purchase1_user2: UserPurchase, purchase2_user2: UserPurchase,
    purchase3_user2: UserPurchase, purchase1_user3: UserPurchase
) -> None:
    '''Проверка на создание рекомендации.'''
    data = {'user_id': str(user1.id)}
    response = await client.post('/generate_recommendations',
                                 json=data)
    response_data = response.json()

    query = select(Recommendation).where(Recommendation.user_id == user1.id)
    result = await async_db.execute(query)
    recommendation = result.scalars().one_or_none()

    assert response_data['status'] == (
        'Рекомендация успешно сгенерирована.')
    assert recommendation is not None
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_get_recomendation(
    client: AsyncClient, async_db: AsyncSession,
    user1: User, user2: User, user3: User,
    item1: Item, item2: Item, item3: Item, item4: Item, item5: Item,
    purchase1_user1: UserPurchase, purchase2_user1: UserPurchase,
    purchase1_user2: UserPurchase, purchase2_user2: UserPurchase,
    purchase3_user2: UserPurchase, purchase1_user3: UserPurchase
) -> None:
    '''Проверка на получение рекомендации пользователя.'''
    data = {'user_id': str(user1.id)}
    response = await client.post('/generate_recommendations',
                                 json=data)

    response = await client.get(f'/recommendations?user_id={user1.id}')

    assert response.status_code == HTTPStatus.OK
