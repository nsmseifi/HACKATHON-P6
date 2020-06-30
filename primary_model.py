import datetime
import time
from uuid import uuid4
from sqlalchemy import Column, Integer, ARRAY, String
from sqlalchemy.dialects.postgresql import UUID
from log import logger, LogMsg

class PrimaryModel():
    creation_date = Column(Integer, nullable=False)
    modification_date = Column(Integer)
    id = Column(UUID,nullable=False, primary_key=True,unique=True)
    version = Column(Integer, default=1)
    tags = Column(ARRAY(String))
    creator = Column(String)
    modifier = Column(String)

    def __init__(self,username=None):
        self.id = str(uuid4())
        self.creation_date = Now()
        self.version = 1
        self.creator = username

    def edit_basic_data(self,username=None):
        self.modifier = username
        self.modification_date = Now()
        self.version +=1

    def populate_data(self,data):
        for key, value in data.items():
            setattr(self, key, value)
        return self

    @classmethod
    def populate(cls,data,username=None):
        instance = cls(username)
        for key, value in data.items():
            setattr(instance, key, value)
        logger.debug(LogMsg.INSTANCE_POPULATED,instance.to_dict())
        return instance

    @classmethod
    def create_query(cls, db_session, *criterion):

        query = db_session.query(cls).filter(*criterion)

        return query

    def to_dict(self):
        logger.debug("primary    CALLED...........")

        res = dict((name, getattr(self, name)) for name in dir(self) if
                   callable(getattr(self,name))==False and
                   name.startswith('_')==False )

        if "metadata" in res:
            del res['metadata']
        return res

def Now():
    now = time.mktime(datetime.datetime.now().timetuple())
    return int(now)