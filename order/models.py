from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import Column, ForeignKey, Float, String, JSON, Integer
from sqlalchemy.orm import relationship

from books.models import Book
from db_session import Base
from enums import OrderStatus
from primary_model import PrimaryModel
from user.models import Person


class Order(PrimaryModel, Base):

    __tablename__ = 'orders'

    person_id = Column(UUID, ForeignKey(Person.id),nullable=False)
    status = Column(ENUM(OrderStatus),nullable=False,default=OrderStatus.Created)
    total_price = Column(Float,default=0.0)
    description = Column(String)
    price_detail = Column(JSON)

    person = relationship(Person, primaryjoin=person_id == Person.id)

    def __init__(self,username):
        super(Order, self).__init__(username)

    def to_dict(self):

        result = {
            'person_id': self.person_id,
            'price_detail': self.price_detail,
            'description': self.description,
            'total_price': self.total_price,
            'creator': self.creator,
            'creation_date': self.creation_date,
            'id': self.id,
            'version': self.version,
            'modification_date': self.modification_date,
            'modifier': self.modifier,
            'tags': self.tags,
        }
        if self.status is None:
            result.update({'status': None})
        else:
            result.update({'status': self.status.name})
        if self.person and self.person is not None:
            result.update({'person': self.person.to_dict()})
        else:
            result.update({'person': None})

        return result


class OrderItem(PrimaryModel, Base):
    __tablename__ = 'order_items'

    order_id = Column(UUID, ForeignKey(Order.id),nullable=False)
    book_id = Column(UUID, ForeignKey(Book.id),nullable=False)
    unit_price = Column(Float,default=0.0)
    discount = Column(Float,default=0.0)
    net_price = Column(Float,default=0.0)
    count = Column(Integer,default=0)
    description = Column(String)
    price_detail = Column(JSON)
    order = relationship(Order, primaryjoin=order_id == Order.id)
    book = relationship(Book, primaryjoin=book_id == Book.id)



    def __init__(self,username):
        super(OrderItem, self).__init__(username)


    def to_dict(self):

        result = {
            'book_id': self.book_id,
            'order_id': self.order_id,
            'description': self.description,
            'unit_price': self.unit_price,
            'discount': self.discount,
            'net_price': self.net_price,
            'count': self.count,
            'price_detail': self.price_detail,
            'creator': self.creator,
            'creation_date': self.creation_date,
            'id': self.id,
            'version': self.version,
            'modification_date': self.modification_date,
            'modifier': self.modifier,
            'tags': self.tags
        }
        return result

