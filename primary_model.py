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
        logger.debug(LogMsg.POPULATING_BASIC_DATA)
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
                           #
                           # (not name.startswith('_')) and not name.startswith(
                           #     'to_dict')and not name.startswith(
                           #     'edit')and not name.startswith(
                           #     'get_by_id')and not name.startswith(
                           #     'populate')and not name.startswith(
                           #     'edit_basic_data')and not name.startswith(
                           #     'mongo') and not name.startswith(
                           #     'create_query')) if not isinstance(self,
                           #                                        dict) else self

        if "metadata" in res:
            del res['metadata']
        return res
    # @classmethod
    # def get_all(cls, db_session, query_params=None, user=None, base_query=None,
    #             extra_filters=None):
    #
    #     if not query_params:
    #         query_params = {}
    #
    #     if base_query:
    #         if 'group' in query_params:
    #             # raise on purpose. this case will be handled if there is any demand
    #             raise HttpError(400,'INVALID_SEARCH_DATA')
    #         query = base_query
    #     else:
    #         if 'group' in query_params:
    #             group_by_terms = [getattr(cls, field) for field in
    #                               query_params['group']]
    #
    #             query = db_session.query(*group_by_terms)
    #         else:
    #             query = db_session.query(cls)
    #
    #     # We have to use `domain_id` and `security_tags` of user in query
    #     if user:
    #         query = cls.add_user_details_to_query(query, user)
    #
    #     # Set default query parameters
    #     query_params.setdefault('filter', {})
    #     if extra_filters:
    #         for k, v in extra_filters.items():
    #             # It may happens that any key in extra filters has conflict with
    #             #   search terms, so in this case, `$and` query must be made
    #             #   including both search conditions
    #             if k in query_params['filter']:
    #                 input_term = query_params['filter'][k]
    #                 # TODO check other types in case of usage
    #
    #                 query_params['filter'][k] = v if isinstance(v, dict) \
    #                     else {'$eq': v}
    #
    #                 query_params['filter'][k].update(input_term
    #                                                  if isinstance(input_term,
    #                                                                dict)
    #                                                  else {'$eq': input_term})
    #
    #             else:
    #                 query_params['filter'][k] = v
    #
    #     if 'count' in query_params or 'group' in query_params:
    #         query_params.pop('sort', None)
    #         query_params.pop('skip', None)
    #         query_params['limit'] = 0
    #     else:
    #         if hasattr(cls, 'create_date'):
    #             query_params.setdefault('sort', ['create_date-'])
    #
    #         query_params.setdefault('skip', 0)
    #         query_params.setdefault('limit', 20)
    #
    #     data = []
    #     meta = {}
    #     try:
    #         result = cls.mongoquery(query).query(**query_params).end().all()
    #         if 'count' in query_params:
    #             meta = {'count': result[0][0]}
    #         elif 'group' in query_params:
    #             if len(query_params['group']) == 1:
    #                 data = [r[0] for r in result]
    #             else:
    #                 for r in result:
    #                     data.append(dict(zip(query_params['group'], r)))
    #         else:
    #             data = result
    #     except (AssertionError, Error) as e:
    #         logger.exception(LogMsg.GET_FAILED,exc_info=True)
    #
    #     return data, meta
    #
    # @classmethod
    # def get_by_id(cls, db_session, entity_id,
    #               extra_criterion=tuple(), joins=tuple()):
    #
    #     query = db_session.query(cls).filter(cls.id == entity_id)
    #
    #     if extra_criterion:
    #         query = query.filter(*extra_criterion)
    #     if joins:
    #         for relation in joins:
    #             query = query.options(joinedload(relation))
    #     return query.first()
    #

def Now():
    now = time.mktime(datetime.datetime.now().timetuple())
    return int(now)