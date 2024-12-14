from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item, User, UserPurchase


@pytest.mark.asyncio
async def test_get_right_recomendation(
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
    response_data = response.json()
    data = response_data['data']['item_id']

    assert (data == str(item3.id) or data == str(item5.id))


@pytest.mark.asyncio
async def test_user_with_no_recs1(
    client: AsyncClient, async_db: AsyncSession,
    user1: User, user2: User, user3: User,
    item1: Item, item2: Item, item3: Item, item4: Item, item5: Item,
    purchase1_user1: UserPurchase, purchase2_user1: UserPurchase,
    purchase1_user2: UserPurchase, purchase2_user2: UserPurchase,
    purchase3_user2: UserPurchase, purchase1_user3: UserPurchase
) -> None:
    '''
    Если у пользователя нет общих покупок с другими пользователями,
    то для него нет рекомендаций.
    '''
    data = {'user_id': str(user3.id)}
    response = await client.post('/generate_recommendations',
                                 json=data)
    response_data = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_data['detail'] == ('Недостаточно данных для '
                                       'составления рекомендации: '
                                       'нет пользователей со '
                                       'схожими покупками.')

    response = await client.get(f'/recommendations?user_id={user3.id}')
    response_data = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response_data['detail'] == ('Нет рекомендаций.')


@pytest.mark.asyncio
async def test_user_with_no_recs2(
    client: AsyncClient, async_db: AsyncSession,
    user1: User, user2: User, user3: User,
    item2: Item, item4: Item,
    purchase2_user1: UserPurchase,
    purchase1_user2: UserPurchase,
    purchase1_user3: UserPurchase
) -> None:
    '''
    Если у пользователей одинаковые покупки,
    то пользователю нечего порекомендовать.
    '''
    data = {'user_id': str(user1.id)}
    response = await client.post('/generate_recommendations',
                                 json=data)
    response_data = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_data['detail'] == ('Недостаточно данных для составления '
                                       'рекомендации: другие пользователи не '
                                       'покупали товары, не купленные данным '
                                       'пользователем.')

    response = await client.get(f'/recommendations?user_id={user1.id}')
    response_data = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response_data['detail'] == ('Нет рекомендаций.')
