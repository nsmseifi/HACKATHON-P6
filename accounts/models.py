from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import Column, ForeignKey, Float
from sqlalchemy.orm import relationship

from db_session import Base
from primary_model import PrimaryModel
from enums import AccountTypes
from user.models import Person


class Account(PrimaryModel, Base):
    __tablename__ = 'accounts'

    person_id = Column(UUID, ForeignKey(Person.id), nullable=False)
    value = Column(Float, default=0.00)
    type = Column(ENUM(AccountTypes), nullable=False)

    person = relationship(Person, primaryjoin=person_id == Person.id, lazy=True)

    def __init__(self, username):
        super(Account, self).__init__(username)

    def to_dict(self):
        data = {
            'id': self.id,
            'person_id': self.person_id,
            'value': self.value,
            'creator': self.creator,
            'creation_date': self.creation_date,
            'version': self.version,
            'modification_date': self.modification_date,
            'modifier': self.modifier,
            'tags': self.tags
        }
        if self.person is not None:
            data.update({'person': self.person.to_dict()})
        if isinstance(self.type, str):
            data.update({'type': self.type})
        else:
            data.update({'type': self.type.value})
        return data
