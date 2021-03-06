from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from db_session import Base
from log import logger, LogMsg
from primary_model import PrimaryModel


class Store(PrimaryModel, Base):
    __tablename__ = 'stores'

    name = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    image = Column(UUID)
    email = Column(String, unique=True, nullable=True)
    store_code = Column(String,unique=True,nullable=False)
    account_id = Column(String)

    def __init__(self, username):
        super(Store, self).__init__(username)

    def to_dict_(self):

        result = {
            'creator': self.creator,
            'creation_date': self.creation_date,
            'id': self.id,
            'version': self.version,
            'modification_date': self.modification_date,
            'modifier': self.modifier,
            'tags': self.tags,
            'address': self.address,
            'store_code': self.store_code,
            'email': self.email,
            'image': self.image,
            'name': self.name,
            'phone': self.phone

        }
        return result
