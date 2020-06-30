from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, Float, JSON

from db_session import Base
from accounts.models import Account
from payment.models import Payment
from primary_model import PrimaryModel


class Transaction(PrimaryModel, Base):

    __tablename__ = 'transactions'

    account_id = Column(UUID, ForeignKey(Account.id),nullable=False)
    credit = Column(Float, default=0.00)
    debit = Column(Float, default=0.00)
    payment_id = Column(UUID,ForeignKey(Payment.id))
    details = Column(JSON)

    def __init__(self,username):
        super(Transaction, self).__init__(username)