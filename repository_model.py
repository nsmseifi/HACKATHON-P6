from helper import Http_error, value
from log import logger, LogMsg
from messages import Message

MAX_DB_QUERY_LIMIT = value('MAX_DB_QUERY_LIMIT', 50)


class BasicRepository():
    def __init__(self, model, db_session, username=None):
        self.model = model
        self.db_session = db_session
        self.username = username

    @classmethod
    def generate(cls, model, db_session, username=None):
        repo = cls(model, db_session, username)
        return repo

    def get_by_id(self, entity_id):
        query = self.db_session.query(self.model).filter(
            self.model.id == entity_id)
        return query.first()

    def check_exists(self, filter_dict):
        query = self.db_session.query(self.model)
        for k, v in filter_dict.items():
            query = query.filter(self.model.k == v)
        return query.first()

    def get_by_data(self, data):
        result = self.model.mongoquery(
            self.db_session.query(self.model)).query(
            **data).end().first()
        return result

    def search_in_tags(self, data):

        query = self.db_session.query(self.model).filter(
            self.model.tags.any(data['tags']))
        if 'person_id' in data:
            query.filter(self.model.person_id == data.get('person_id'))
        if 'status' in data:
            query.filter(self.model.status == data.get('status'))
        result = query.order_by(self.model.creation_date.desc()).all()
        return result

    def get_all_by_data(self, data):
        if data.get('sort') is None:
            data['sort'] = ['creation_date-']
        if 'join' in data.keys():
            del data['join']
        if 'limit' in data.keys():
            data['limit'] = min(int(data.get('limit')), int(MAX_DB_QUERY_LIMIT))

        result = self.model.mongoquery(
            self.db_session.query(self.model)).query(
            **data).end().all()
        return result

    def count_of_table(self):
        result = self.db_session.query(self.model.id).count()
        return result

    def add(self, data):
        instance = self.model.populate(data, self.username)
        self.db_session.add(instance)
        self.db_session.flush()
        return instance

    def update_by_instance(self, instance, data):
        self.version_check(instance, data.get('version'))
        instance.populate_data(data)
        instance.edit_basic_data(self.username)
        return instance

    def update_by_id(self, id, data):
        instance = self.get_by_id(id)
        if instance is None:
            logger.error(LogMsg.NOT_FOUND, {'instance_id': id})
            return False
        self.version_check(instance, data.get('version'))

        instance.populate_data(data)
        instance.edit_basic_data(self.username)
        logger.debug(LogMsg.EDIT_SUCCESS, instance.to_dict())
        return instance

    def delete_by_model(self, model_instance, version=None):
        self.version_check(model_instance, version)

        self.db_session.delete(model_instance)
        return True

    def delete_by_id(self, id, version=None):
        model_instance = self.get_by_id(id)
        if version:
            self.version_check(model_instance, version)

        self.db_session.delete(model_instance)
        return True

    def delete_all_by_data(self, data):
        self.model.mongoquery(
            self.db_session.query(self.model)).query(
            **data).end().delete()
        return True

    def get_all(self, data):
        if data.get('sort') is None:
            data['sort'] = ['creation_date-']
        if 'join' in data.keys():
            del data['join']
        if 'limit' in data.keys():
            data['limit'] = min(int(data.get('limit')), int(MAX_DB_QUERY_LIMIT))

        result = self.model.mongoquery(
            self.db_session.query(self.model)).query(
            **data).end().all()

        return result

    def version_check(self, model, version=None):
        if version is not None:
            if model.version != version:
                logger.error(LogMsg.VERSION_CONFLICT)
                raise Http_error(409, Message.VERSION_CONFLICT)
