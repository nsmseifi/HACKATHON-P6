from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db_session import Base
from log import logger, LogMsg
from primary_model import PrimaryModel


class Person(PrimaryModel, Base):
    __tablename__ = 'persons'

    name = Column(String, nullable=False)
    last_name = Column(String)
    full_name = Column(String)
    address = Column(String)
    phone = Column(String)
    image = Column(UUID)
    email = Column(String, unique=True, nullable=True)
    cell_no = Column(String, unique=True)
    current_book_id = Column(UUID)
    bio = Column(String)
    is_legal = Column(Boolean, default=False)

    def __init__(self, username):
        super(Person, self).__init__(username)

    @classmethod
    def populate(cls, data, username=None):
        logger.debug(LogMsg.POPULATING_BASIC_DATA)
        instance = cls(username)
        for key, value in data.items():
            setattr(instance, key, value)
        cls.set_full_name(instance)
        logger.debug(LogMsg.INSTANCE_POPULATED, instance.to_dict())
        return instance

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
            'bio': self.bio,
            'cell_no': self.cell_no,
            'current_book_id': self.current_book_id,
            'email': self.email,
            'image': self.image,
            'name': self.name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone': self.phone

        }
        if self.is_legal is None:
            result['is_legal'] = False
        else:
            result['is_legal'] = self.is_legal
        return result

    @staticmethod
    def set_full_name(instance):
        if instance.name is None or (instance.name == ''):
            instance.full_name = instance.last_name
        elif instance.last_name is None or (instance.last_name == ''):
            instance.full_name = instance.name
        else:
            instance.full_name = '{} {}'.format(instance.name, instance.last_name)
        return instance.full_name



class User(PrimaryModel, Base):
    __tablename__ = 'users'
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    person_id = Column(UUID, ForeignKey('persons.id'))

    person = relationship(Person, primaryjoin=person_id == Person.id, lazy=True)

    def __init__(self, username):
        super(User, self).__init__(username)

    def to_dict(self):
        logger.debug("CALLED...........")
        result = {
            'username': self.username,
            'creator': self.creator,
            'creation_date': self.creation_date,
            'id': self.id,
            'person_id': self.person_id,
            'version': self.version,
            'modification_date': self.modification_date,
            'modifier': self.modifier,
            'tags': self.tags
        }
        if self.person is None:
            result.update({'person':None})
        else:
            result.update({'person': self.person.to_dict()})

        return result
