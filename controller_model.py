from check_permission import get_user_permissions, has_permission, \
    validate_permissions_and_access
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
        logger.debug(LogMsg.SCHEMA_CHECKED)
        if self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('add'),
                                  access_level=access_level, special_data=special_data)
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
        if self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('get'),
                                  result, access_level=access_level,
                                  special_data=special_data)

        return result

    def edit(self, id, data, db_session, username=None, schema_checked=False,
             permission_checked=False, access_level=None, special_data={}):
        logger.debug(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        if self.schemas is not None and not schema_checked:
            schema_validate(data, self.schemas.get('edit'))
        logger.debug(LogMsg.SCHEMA_CHECKED)
        result = repository_ins.update_by_id(id, data)
        if result is False:
            logger.error(LogMsg.NOT_FOUND, {'id': id})
            raise Http_error(404, Message.NOT_FOUND)

        logger.debug(LogMsg.EDIT_SUCCESS, result.to_dict())
        if self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('edit'),
                                  result, access_level=access_level,
                                  special_data=special_data)

        logger.info(LogMsg.END)
        return result

    def edit_by_model(self, model, data, db_session, username=None, schema_checked=False,
                      permission_checked=False, access_level=None, special_data={}):
        logger.debug(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        if self.schemas is not None and not schema_checked:
            schema_validate(data, self.schemas.get('edit'))
        logger.debug(LogMsg.SCHEMA_CHECKED)
        if self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('edit'),
                                  model, access_level=access_level,
                                  special_data=special_data)

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
        if self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('delete'),
                                  model_instance, access_level=access_level,
                                  special_data=special_data)
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
        if self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('delete'),
                                  model, access_level=access_level,
                                  special_data=special_data)
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
        if self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('get'),
                                  access_level=access_level, special_data=special_data)
        result = repository_ins.get_all(data)
        return result

    def search_in_tags(self, data, db_session, username=None, permission_checked=False,
                       access_level=None, special_data={}):
        logger.info(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        if self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('get'),
                                  access_level=access_level, special_data=special_data)
        result = repository_ins.search_in_tags(data)
        return result

    def delete_all_by_data(self, data, db_session, username=None,
                           permission_checked=False, access_level=None,
                           special_data={}):
        logger.info(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        if username is not None and self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('get'),
                                  access_level=access_level, special_data=special_data)
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
        if self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('get'),
                                  result, access_level=access_level,
                                  special_data=special_data)

        return result

    def get_all_by_data(self, data, db_session, username=None, permission_checked=False,
                        access_level=None, special_data={}):
        logger.info(LogMsg.START, username)
        repository_ins = self.repository.generate(self.model, db_session, username)
        result = repository_ins.get_all_by_data(data)
        if self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('get'),
                                  access_level=access_level, special_data=special_data)

        return result

    def execute_query_data(self, data, db_session, username=None,
                           permission_checked=False):
        logger.info(LogMsg.START, username)
        skip = data.get('skip', 0)
        limit = data.get('limit', MAX_DB_QUERY_LIMIT)
        limit = min(int(limit), int(MAX_DB_QUERY_LIMIT))
        has_more = False
        data['limit'] = limit + 1
        repository_ins = self.repository.generate(self.model, db_session, username)
        result = repository_ins.get_all_by_data(data)
        if len(result) > limit:
            has_more = True
            del result[-1]
        if self.permissions is not None and not permission_checked:
            self.check_permission(db_session, username, self.permissions.get('get'))
        res_dict = [item.to_dict() for item in result]

        final_res = dict(result=res_dict, has_more=has_more)
        logger.debug(LogMsg.QUERY_DATA_IS, final_res)
        return final_res

    def check_permission(self, db_session, username=None, permission_string=None,
                         model=None, access_level=None, special_data={}):
        if permission_string is not None and username is not None:
            logger.debug(LogMsg.PERMISSION_CHECK, username)
            validate_permissions_and_access(username, db_session,
                                            permission_string, special_data=special_data,
                                            model=model,
                                            access_level=access_level)
            logger.debug(LogMsg.PERMISSION_VERIFIED, username)
        return True
