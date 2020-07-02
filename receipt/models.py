from sqlalchemy import Column, String, JSON, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from db_session import Base
from primary_model import PrimaryModel


class Receipt(PrimaryModel, Base):
    __tablename__ = 'receipts'

    title = Column(String)
    payee_id = Column(UUID,  nullable=False)
    payer_id = Column(UUID,  nullable=True)
    payer_name = Column(String)
    body = Column(JSON, nullable=False)
    total_payment = Column(Float, unique=True, nullable=True)
    subtotal = Column(Float, unique=True, nullable=True)
    hst = Column(Float, unique=True, nullable=True)

    details = Column(JSON)
    status = Column(String, default='Waiting', nullable=False)

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
            'details':self.details,
            'subtotal':self.subtotal,
            'hst':self.hst
        }
        return result
