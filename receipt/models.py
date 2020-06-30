from sqlalchemy import Column, String, JSON, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db_session import Base
from primary_model import PrimaryModel
from store.models import Store
from user.models import Person


class Receipt(PrimaryModel, Base):
    __tablename__ = 'receipts'

    title = Column(String, nullable=False)
    payee_id = Column(UUID,  nullable=False)
    payer_id = Column(UUID,  nullable=True)
    payer_name = Column(String)
    body = Column(JSON, nullable=False)
    total_payment = Column(Integer, unique=True, nullable=True)
    details = Column(JSON)
    status = Column(String, default='Waiting to Pay', nullable=False)

    # payee = relationship(Store, lazy=True)
    # payer = relationship(Store, primaryjoin=payer_id == Person.id, lazy=True)

    def __init__(self, username):
        super(Receipt, self).__init__(username)

    def to_dict_(self):
        result = {
            'creator': self.creator,
            'creation_date': self.creation_date,
            'id': self.id,
            'version': self.version,
            'modification_date': self.modification_date,
            'modifier': self.modifier,
            'tags': self.tags,
            'title':self.title,
            'payee_id': self.payee_id,
            'payer_name':self.payer_name,
            'payer_id': self.payer_id,
            'status':self.status,
            'body':self.body,
            'total_payment':self.total_payment,
            'details':self.details
        }
        return result
