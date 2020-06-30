from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, Float, String, JSON, Boolean
from sqlalchemy.orm import relationship

from accounts.models import Account
from user.models import Person
from db_session import Base
from primary_model import PrimaryModel


class Payment(PrimaryModel, Base):
    __tablename__ = 'payments'
    person_id = Column(UUID, ForeignKey(Person.id))
    amount = Column(Float, nullable=False)
    shopping_key = Column(String)
    reference_code = Column(String)
    details = Column(JSON)
    order_details = Column(JSON)
    agent = Column(String)
    used = Column(Boolean, default=False)
    status = Column(String)

    def __init__(self, username):
        super(Payment, self).__init__(username)


class CheckoutPressAccount(PrimaryModel, Base):
    __tablename__ = 'checkout_press_accounts'
    amount = Column(Float, nullable=False)
    payer_id = Column(UUID, ForeignKey(Person.id), nullable=False)
    receiver_id = Column(UUID, ForeignKey(Person.id), nullable=False)
    receiver_account_id = Column(UUID, ForeignKey(Account.id))
    payment_details = Column(JSON)

    receiver = relationship(Person, primaryjoin=receiver_id == Person.id, lazy=True)

    def __init__(self, username):
        super(CheckoutPressAccount, self).__init__(username)

    def to_dict(self):
        result = {
            'creator': self.creator,
            'creation_date': self.creation_date,
            'id': self.id,
            'version': self.version,
            'modification_date': self.modification_date,
            'modifier': self.modifier,
            'tags': self.tags,
            'amount': self.amount,
            'payer_id': self.payer_id,
            'receiver_id': self.receiver_id,
            'receiver_account_id': self.receiver_account_id,
            'payment_details': self.payment_details,

        }
        if self.receiver is None:
            result.update({'receiver':None})
        else:
            result.update({'receiver': self.receiver.to_dict()})

        return result
