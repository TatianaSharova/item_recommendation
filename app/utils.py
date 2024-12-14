import uuid

import pandas as pd
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserPurchase


async def find_similar_users_purchases(user_item_ids: list[uuid.UUID],
                                       user_id: uuid.UUID,
                                       session: AsyncSession):
    '''Находим пользователей, которые покупали такие же товары.'''
    query = select(UserPurchase.user_id, UserPurchase.item_id).where(
        and_(
            UserPurchase.item_id.in_(user_item_ids),
            UserPurchase.user_id != user_id)).group_by(
                UserPurchase.user_id, UserPurchase.item_id)
    result = await session.execute(query)
    return result.fetchall()


async def find_similar_users(user_item_ids: list[uuid.UUID],
                             user_id: uuid.UUID,
                             session: AsyncSession):
    '''Находим пользователей, которые покупали такие же товары.'''
    query = select(
        UserPurchase.user_id
    ).where(and_(
        UserPurchase.item_id.in_(user_item_ids),
        UserPurchase.user_id != user_id)).group_by(UserPurchase.user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_purchases_dataframe(session: AsyncSession,
                                  query) -> pd.DataFrame:
    '''
    Получаем DataFrame из базы данных
    и делим его на столбцы user_id и item_id.
    '''
    result = await session.execute(query)
    purchases_df = pd.DataFrame(result.fetchall(), columns=result.keys())
    purchases_df['UserPurchase'] = purchases_df['UserPurchase'].astype(str)
    purchases_df = purchases_df['UserPurchase'].str.split(' купил ',
                                                          expand=True)
    purchases_df.columns = ['user_id', 'item_id']
    return purchases_df
