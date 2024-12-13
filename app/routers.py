import uuid

from app.db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from app.orm_query import (ItemRepository, PurchaseRepository, RecommendRepository,
                       UserRepository)
from app.schemas import ItemAdd, PurchaseAdd, RecommendationAdd, UserAdd
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(
    prefix='/users',
    tags=['пользователи']
)

item_router = APIRouter(
    prefix='/items',
    tags=['товары']
)

purchase_router = APIRouter(
    prefix='/purchases',
    tags=['заказы']
)


gen_recommendation_router = APIRouter(
    prefix='/generate_recommendations',
    tags=['создать рекомендации']
)

recommendation_router = APIRouter(
    prefix='/recommendations',
    tags=['рекомендации']
)


@user_router.post('', status_code=status.HTTP_201_CREATED)
async def add_user(user: UserAdd, session: AsyncSession = Depends(get_db)):
    '''Создать нового пользователя.'''
    user_id = await UserRepository.add_user(user, session)
    return {'status': 'Пользователь создан.', 'user_id': user_id}


@user_router.get('')
async def get_users(session: AsyncSession = Depends(get_db)):
    '''Посмотреть всех пользователей.'''
    users = await UserRepository.get_all(session)
    return {'data': users}


@item_router.post('', status_code=status.HTTP_201_CREATED)
async def add_item(item: ItemAdd,
                   session: AsyncSession = Depends(get_db)):
    '''Создание нового товара.'''
    item_id = await ItemRepository.add_item(item, session)
    return {'status': 'Товар создан.',
            'item_id': item_id,
            'data': item}


@item_router.get('')
async def get_items(session: AsyncSession = Depends(get_db)):
    '''Просмотреть все товары.'''
    items = await ItemRepository.get_all(session)
    return {'data': items}


@item_router.get('/{item_id}')
async def get_item(item_id: str, session: AsyncSession = Depends(get_db)):
    '''Просмотреть товар по id.'''
    try:
        item_id_uuid = uuid.UUID(item_id)
    except ValueError:
        raise HTTPException(status_code=400, detail='Неверный формат id.')
    item = await ItemRepository.get_item(item_id_uuid, session)
    return {'data': item}


@purchase_router.post('', status_code=status.HTTP_201_CREATED)
async def add_purchase(purchase: PurchaseAdd,
                       session: AsyncSession = Depends(get_db)):
    '''Добавить покупку пользователя.'''
    purchase_status = await PurchaseRepository.add_purchase(purchase, session)
    return {'status': purchase_status}


@purchase_router.get('')
async def get_purchases(session: AsyncSession = Depends(get_db)):
    '''Просмотреть все покупки.'''
    purchases = await PurchaseRepository.get_all(session)
    return {'data': purchases}


@purchase_router.get('/{user_id}')
async def get_user_purchases(user_id: str,
                             session: AsyncSession = Depends(get_db)):
    '''Просмотреть все покупки определенного пользователя.'''
    try:
        user_id_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail='Неверный формат id.')
    user_purchases = await PurchaseRepository.get_user_purchases(user_id_uuid,
                                                                 session)
    return {'data': user_purchases}


@gen_recommendation_router.post('', status_code=status.HTTP_201_CREATED)
async def add_request_for_recommendation(
    user: RecommendationAdd, session: AsyncSession = Depends(get_db)
):
    '''Создаем рекомендацию для пользователя.'''
    recommendation = await RecommendRepository.add_recommendation(user,
                                                                  session)
    return {'status': f'{recommendation}'}


@recommendation_router.get('')
async def get_user_recommendation(user_id: str,
                                  session: AsyncSession = Depends(get_db)):
    '''Просмотреть рекомендацию товара пользователю.'''
    try:
        user_id_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail='Неверный формат id.')
    recommendation = await RecommendRepository.get_recommendation(
        user_id_uuid, session)
    return {'data': recommendation}
