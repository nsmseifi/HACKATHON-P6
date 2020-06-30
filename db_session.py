from contextlib import contextmanager
from uuid import uuid4

from mongosql import MongoSqlBase
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.sql.functions import now
import sqlalchemy

from configs import DATABASE_URI


# DECLARATIVE `Base` DEFINITION

__metadata = MetaData(naming_convention={'pk': 'pk_tb_%(table_name)s',
                                         'fk': 'fk_tb_%(table_name)s_col_%(column_0_name)s',
                                         'ix': 'ix_tb_%(table_name)s_col_%(column_0_name)s',
                                         'uq': '%(table_name)s_id_key'})
Base = declarative_base(cls=(MongoSqlBase,), metadata=__metadata)

class CastingArray(ARRAY):
    def bind_expression(self, bindvalue):
        return sqlalchemy.cast(bindvalue, self)

# SESSION ENGINE

engine = create_engine(DATABASE_URI)

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
db_session = Session()


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
