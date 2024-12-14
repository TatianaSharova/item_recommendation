import uuid

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Model(DeclarativeBase):
    pass


class UUIDModelBase(Model):
    '''Базовая модель для модель для моделей с UUID.'''
    __abstract__ = True
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
        unique=True, nullable=False)


class User(UUIDModelBase):
    '''Модель для пользователя.'''
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String(40), unique=True,
                                          nullable=False)

    recommendations: Mapped[list['Recommendation']] = relationship(
        lazy='selectin', back_populates='user', cascade='all, delete-orphan'
    )
    purchases: Mapped[list['UserPurchase']] = relationship(
        lazy='selectin', back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return self.username


class Item(UUIDModelBase):
    '''Модель для товара.'''
    __tablename__ = 'item'

    name: Mapped[str] = mapped_column(String(40), nullable=False)
    category: Mapped[str] = mapped_column(String(40), nullable=False)

    purchases: Mapped[list['UserPurchase']] = relationship(
        lazy='selectin', back_populates='item', cascade='all, delete-orphan'
    )
    recommendations: Mapped[list['Recommendation']] = relationship(
        lazy='selectin', back_populates='item', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'Товар {self.name} из категории {self.category}.'


class Recommendation(UUIDModelBase):
    '''Модель для рекомендаций.'''
    __tablename__ = 'recommendation'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id',
                                                     ondelete='CASCADE'))
    item_id: Mapped[UUID] = mapped_column(ForeignKey('item.id',
                                                     ondelete='CASCADE'))

    user: Mapped['User'] = relationship(lazy='selectin',
                                        back_populates='recommendations')
    item: Mapped['Item'] = relationship(lazy='selectin',
                                        back_populates='recommendations')

    def __repr__(self) -> str:
        return (f'Пользователю {self.user_id} '
                f'можно порекомендовать {self.item_id}.')


class UserPurchase(UUIDModelBase):
    '''Модель для покупки пользователя.'''
    __tablename__ = 'userpurchase'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id',
                                                     ondelete='CASCADE'))
    item_id: Mapped[UUID] = mapped_column(ForeignKey('item.id',
                                                     ondelete='CASCADE'))
    category: Mapped[str] = mapped_column(String(40), nullable=False)
    purchase_date: Mapped[DateTime] = mapped_column(DateTime,
                                                    default=func.now())

    user: Mapped['User'] = relationship(lazy='selectin',
                                        back_populates='purchases')
    item: Mapped['Item'] = relationship(lazy='selectin',
                                        back_populates='purchases')

    def __repr__(self) -> str:
        return f'{self.user_id} купил {self.item_id}'
