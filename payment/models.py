from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, Float, String, JSON, Boolean
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

