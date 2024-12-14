import uuid
from collections import Counter

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item, Recommendation, User, UserPurchase
from app.schemas import (ItemAdd, ItemRead, PurchaseAdd, PurchaseRead,
                         RecommendationAdd, RecommendationRead, UserAdd,
                         UserRead)
from app.utils import get_purchases_dataframe


class UserRepository:
    '''Методы для работы с пользователями.'''
    @classmethod
    async def add_user(cls, user: UserAdd,
                       session: AsyncSession) -> int:
        '''Создание нового пользователя.'''
        data = user.model_dump()
        new_user = User(**data)
        try:
            session.add(new_user)
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=400,
                detail='Пользователь с таким именем уже существует.')
        return new_user.id

    @classmethod
    async def get_user(cls, user_id: uuid.UUID,
                       session: AsyncSession) -> ItemRead:
        '''Возвращает пользователя.'''
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            raise HTTPException(status_code=404,
                                detail='Пользователь не существует.')
        return UserRead.model_validate(user_model)

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[UserRead]:
        '''Возвращвет список всех пользователей.'''
        query = select(User)
        result = await session.execute(query)
        user_models = result.scalars().all()
        users = [UserRead.model_validate(
            user_model
        ) for user_model in user_models]
        return users


class ItemRepository:
    '''Методы для работы с товарами.'''
    @classmethod
    async def add_item(cls, item: ItemAdd,
                       session: AsyncSession) -> int:
        '''Создание нового товара.'''
        data = item.model_dump()
        new_item = Item(**data)
        session.add(new_item)
        await session.commit()
        return new_item.id

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[ItemRead]:
        '''Возвращает список всех товаров.'''
        query = select(Item)
        result = await session.execute(query)
        item_models = result.scalars().all()
        items = [ItemRead.model_validate(
            item_model
        ) for item_model in item_models]
        return items

    @classmethod
    async def get_item(cls, item_id: uuid.UUID,
                       session: AsyncSession) -> ItemRead:
        '''Возвращает товар.'''
        query = select(Item).where(Item.id == item_id)
        result = await session.execute(query)
        item_model = result.scalar_one_or_none()

        if item_model is None:
            raise HTTPException(status_code=404,
                                detail=f'Товар {item_id} не найден.')
        return ItemRead.model_validate(item_model)


class PurchaseRepository:
    '''Методы для работы с покупками.'''

    @classmethod
    async def add_purchase(cls, purchase: PurchaseAdd,
                           session: AsyncSession) -> str:
        '''Создание новой покупки.'''
        for item in purchase.cart:
            exist_item = await ItemRepository.get_item(item.id, session)
            if exist_item.category != item.category:
                raise HTTPException(
                    status_code=400,
                    detail=(f'Категория не соответствует товару. '
                            f'Категория товара {item.id} - '
                            f'{exist_item.category}'))

            new_purchase = UserPurchase(
                user_id=purchase.user_id,
                item_id=item.id,
                category=item.category
            )
            session.add(new_purchase)

        await session.commit()
        return (f'Покупка для пользователя '
                f'{purchase.user_id} успешно добавлена.')

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[PurchaseRead]:
        '''Возвращает список всех покупок.'''
        query = select(UserPurchase)
        result = await session.execute(query)
        purchase_models = result.scalars().all()
        purchases = [PurchaseRead.model_validate(
            purchase_model
        ) for purchase_model in purchase_models]
        return purchases

    @classmethod
    async def get_user_purchases(cls, user_id: uuid.UUID,
                                 session: AsyncSession) -> list[PurchaseRead]:
        '''Возвращает список всех покупок определенного пользователя.'''
        exist_user = await UserRepository.get_user(user_id, session)

        query = select(UserPurchase).where(
            UserPurchase.user_id == exist_user.id)
        result = await session.execute(query)
        purchase_models = result.scalars().all()
        if purchase_models:
            purchases = [PurchaseRead.model_validate(
                purchase_model
            ) for purchase_model in purchase_models]
            return purchases
        return 'У пользователя нет покупок.'


class RecommendRepository:
    '''Класс для работы с рекомендациями.'''

    @classmethod
    async def get_recommendation(cls, user_id: uuid.UUID,
                                 session: AsyncSession) -> RecommendationRead:
        '''Возвращает рекомендацию.'''
        query = select(Recommendation).where(Recommendation.user_id == user_id)
        result = await session.execute(query)
        recom_model = result.scalar_one_or_none()

        if recom_model is None:
            raise HTTPException(status_code=404, detail='Нет рекомендаций.')
        return RecommendationRead(item_id=recom_model.item_id)

    @classmethod
    async def add_recommendation(cls, user: RecommendationAdd,
                                 session: AsyncSession) -> int:
        '''Создание рекомендации.'''
        exist_user = await UserRepository.get_user(user.user_id, session)

        df = await get_purchases_dataframe(
            session,
            select(UserPurchase)
        )
        # Ищем покупки пользователя
        usr_ps = df[
            df['user_id'] == str(exist_user.id)
        ]['item_id'].tolist()

        # Ищем пользователей со схожими покупками
        similar_users = df[
            df['item_id'].isin(usr_ps) & (df['user_id'] != str(exist_user.id))
        ]
        if similar_users.empty:
            raise HTTPException(
                status_code=400,
                detail=('Недостаточно данных для составления рекомендации: '
                        'нет пользователей со схожими покупками.'))
        similar_users = similar_users['user_id'].tolist()

        # Ищем покупки пользователей со схожим вкусом
        users_purchases = df[
            df['user_id'].isin(similar_users) & ~df['item_id'].isin(usr_ps)]
        if users_purchases.empty:
            raise HTTPException(
                status_code=400,
                detail=('Недостаточно данных для составления рекомендации: '
                        'другие пользователи не покупали товары, не купленные'
                        ' данным пользователем.'))

        # Подсчитываем популярность полученных товаров
        items = users_purchases['item_id'].tolist()
        item_popularity = Counter(items)

        # Получаем список товаров, отсортированных по популярности
        recommended_items = [item for item, _ in item_popularity.most_common()]

        if recommended_items:
            # Возвращаем самый популярный товар для рекомендации
            try:
                recom = await cls.get_recommendation(exist_user.id,
                                                     session)
                if recom.item_id != recommended_items[0]:
                    recom.item_id = recommended_items[0]
                    await session.commit()
            except HTTPException:
                new_recom = Recommendation(
                    user_id=exist_user.id,
                    item_id=uuid.UUID(recommended_items[0]))
                session.add(new_recom)
                await session.commit()
            return 'Рекомендация успешно сгенерирована.'
        else:
            return ('Нет товаров для рекомендации. ')
