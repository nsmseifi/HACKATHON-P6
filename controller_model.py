
from helper import Http_response, Http_error, value
from infrastructure.schema_validator import schema_validate
from log import logger, LogMsg
from messages import Message

MAX_DB_QUERY_LIMIT = value('MAX_DB_QUERY_LIMIT', 50)


class BasicController():

    def __init__(self, model, repository_model, schemas=None, permissions=None):
        self.model = model
        self.repository = repository_model
        self.schemas = schemas
        self.permissions = permissions

    def add(self, data, db_session, username=None, schema_checked=False,
            permission_checked=False, access_level=None, special_data=None):
        logger.debug(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        logger.info(LogMsg.START, username)

        if self.schemas is not None and not schema_checked:
            schema_validate(data, self.schemas.get('add'))
        result = repository_ins.add(data)
        logger.debug(LogMsg.DB_ADD)

        logger.info(LogMsg.END)
        return result

    def get(self, id, db_session, username=None, permission_checked=False,
            access_level=None, special_data={}):
        logger.info(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        result = repository_ins.get_by_id(id)
        if result is None:
            logger.error(LogMsg.NOT_FOUND, {'instance_id': id})
            raise Http_error(404, Message.NOT_FOUND)

        return result

    def edit(self, id, data, db_session, username=None, schema_checked=False,
             permission_checked=False, access_level=None, special_data={}):
        logger.debug(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        if self.schemas is not None and not schema_checked:
            schema_validate(data, self.schemas.get('edit'))
        result = repository_ins.update_by_id(id, data)
        if result is False:
            logger.error(LogMsg.NOT_FOUND, {'id': id})
            raise Http_error(404, Message.NOT_FOUND)


        logger.info(LogMsg.END)
        return result

    def edit_by_model(self, model, data, db_session, username=None, schema_checked=False,
                      permission_checked=False, access_level=None, special_data={}):
        logger.debug(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        if self.schemas is not None and not schema_checked:
            schema_validate(data, self.schemas.get('edit'))

        result = repository_ins.update_by_instance(model, data)
        logger.debug(LogMsg.EDIT_SUCCESS, result.to_dict())

        logger.info(LogMsg.END)
        return result

    def delete(self, id, db_session, username=None, permission_checked=False,
               access_level=None, special_data={}):
        logger.debug(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        model_instance = repository_ins.get_by_id(id)
        if model_instance is None:
            logger.error(LogMsg.NOT_FOUND, {'model_instance_id': id})
            raise Http_error(404, Message.NOT_FOUND)
        try:
            repository_ins.delete_by_model(model_instance)
            logger.debug(LogMsg.DELETE_SUCCESS)
        except:
            logger.error(LogMsg.DELETE_FAILED, exc_info=True)
            raise Http_error(404, Message.NOT_FOUND)

        return Http_response(204, True)

    def delete_by_model(self, model, db_session, username=None, permission_checked=False,
                        access_level=None, special_data={}):
        logger.debug(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        try:
            repository_ins.delete_by_model(model)
            logger.debug(LogMsg.DELETE_SUCCESS)
        except:
            logger.error(LogMsg.DELETE_FAILED, exc_info=True)
            raise Http_error(404, Message.NOT_FOUND)

        return Http_response(204, True)

    def get_all(self, data, db_session, username=None, permission_checked=False,
                access_level=None, special_data={}):
        logger.info(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        result = repository_ins.get_all(data)
        return result

    def search_in_tags(self, data, db_session, username=None, permission_checked=False,
                       access_level=None, special_data={}):
        logger.info(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        result = repository_ins.search_in_tags(data)
        return result

    def delete_all_by_data(self, data, db_session, username=None,
                           permission_checked=False, access_level=None,
                           special_data={}):
        logger.info(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        logger.debug('going to delete all by data {}'.format(data))
        result = repository_ins.delete_all_by_data(data)
        logger.debug('ended deleting all...')
        if not result:
            logger.error(LogMsg.DELETE_FAILED)
            raise Http_error(404, Message.DELETE_FAILED)
        return Http_response(204, True)

    def get_by_data(self, data, db_session, username=None, permission_checked=False,
                    access_level=None, special_data={}):
        logger.info(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        result = repository_ins.get_by_data(data)
        return result

    def get_all_by_data(self, data, db_session, username=None, permission_checked=False,
                        access_level=None, special_data={}):
        logger.info(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        result = repository_ins.get_all_by_data(data)
        return result

    def check_permission(self, db_session, username=None, permission_string=None,
                         model=None, access_level=None, special_data={}):

        return True
