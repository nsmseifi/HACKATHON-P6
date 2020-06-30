from sqlalchemy import Column, String, Integer
from db_session import Base
from primary_model import PrimaryModel


class APP_Token(PrimaryModel, Base):
    __tablename__ = 'app_tokens'
    username = Column(String, nullable=False)
    expiration_date = Column(Integer, nullable=False)

    def __init__(self, username):
        super(APP_Token, self).__init__(username)
