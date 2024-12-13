import datetime as dt
import uuid
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class BaseRead(BaseModel):
    '''Базовая схема для чтения.'''
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class UserAdd(BaseModel):
    '''Схема добавления пользователя.'''
    username: str = Field(..., min_length=1, max_length=40,
                          description='Имя пользователя')


class UserRead(UserAdd, BaseRead):
    '''Схема чтения пользователя.'''
    pass


class ItemAdd(BaseModel):
    '''Схема добавления товара.'''
    name: str = Field(..., min_length=1, max_length=40,
                      description='Название товара')
    category: str = Field(..., min_length=1, max_length=40,
                          description='Категория')


class ItemRead(ItemAdd, BaseRead):
    '''Схема чтения товара.'''
    pass


class ItemInPurchaseAdd(BaseModel):
    '''Схема для добавления товара внутри покупки.'''
    id: uuid.UUID
    category: str = Field(..., min_length=1, max_length=40,
                          description='Категория')


class PurchaseAdd(BaseModel):
    '''Схема добавления покупки.'''
    user_id: uuid.UUID
    cart: List[ItemInPurchaseAdd]


class PurchaseRead(BaseRead):
    '''Схема для чтения покупки.'''
    user_id: uuid.UUID
    item_id: uuid.UUID
    category: str = Field(..., min_length=1, max_length=40,
                          description='Категория')
    purchase_date: dt.datetime


class RecommendationAdd(BaseModel):
    '''Схема для создания рекомендации для пользователя.'''
    user_id: uuid.UUID


class RecommendationRead(BaseModel):
    '''Схема для чтения рекомендации.'''
    item_id: uuid.UUID
