import os
from random import randint
from controller_model import BasicController
from helper import Http_error, Http_response
from log import LogMsg, logger
from messages import Message
from .models import Store
from configs import SIGNUP_USER
from .constants import STORE_ADD_SCHEMA_PATH
from .repository import StoreRepository

save_path = os.environ.get('save_path')

store_schemas = dict(add=STORE_ADD_SCHEMA_PATH)


class StoreController(BasicController):

    def __init__(self):
        super(StoreController, self).__init__(Store, StoreRepository, store_schemas)

    def add(self, db_session, data, username=None, schema_checked=False,
            permission_checked=False):
        logger.info(LogMsg.START, username)

        name = data.get('name')
        data['store_code'] = '{}-{}'.format(name, randint(1000000, 9999999))
        model_instance = super(StoreController, self).add(data, db_session, username,
                                                          schema_checked,
                                                          permission_checked)
        logger.info(LogMsg.END)
        return model_instance.to_dict()

    def get(self, id, db_session, username=None, permission_checked=False):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.MODEL_GETTING)
        store = super(StoreController, self).get(id, db_session, username,
                                                 permission_checked)
        return store.to_dict()

    def edit(self, id, db_session, data, username, permission_checked=False):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.EDIT_REQUST, {'store_id': id, 'data': data})
        model_instance = super(StoreController, self).get(id, db_session)
        if 'store_code' in data:
            del data['store_code']
        if 'id' in data:
            del data['id']
        if 'name' in data:
            data['store_code'] = '{}-{}'.format(data['name'], randint(1000000, 9999999))
        try:
            super(StoreController, self).edit(id, data, db_session, username,
                                              permission_checked)

            logger.debug(LogMsg.MODEL_ALTERED, model_instance.to_dict())

            # TODO change def unique
        except:
            logger.exception(LogMsg.EDIT_FAILED, exc_info=True)
            raise Http_error(500, Message.DELETE_FAILED)

        logger.info(LogMsg.END)
        return model_instance.to_dict()

    def delete(self, id, db_session, username, permission_checked=False):
        logger.info(LogMsg.START, username)

        logger.info(LogMsg.DELETE_REQUEST, {'store_id': id})
        try:
            super(StoreController, self).delete(id, db_session, username,
                                                permission_checked)

        except Exception as e:
            logger.exception(LogMsg.DELETE_FAILED, exc_info=True)
            raise Http_error(500, Message.DELETE_FAILED)

        logger.info(LogMsg.END)

        return Http_response(204, True)

    def get_all(self, db_session, username, permission_checked=False):
        logger.info(LogMsg.START, username)
        try:
            result = super(StoreController, self).get_all({}, db_session, username,
                                                          permission_checked)
            logger.debug(LogMsg.GET_SUCCESS)
        except:
            logger.error(LogMsg.GET_FAILED)
            raise Http_error(400, LogMsg.GET_FAILED)
        logger.debug(LogMsg.END)
        return result

    def search_store(self, data, db_session, username, permission_checked=False):
        logger.info(LogMsg.START, username)
        logger.debug(LogMsg.GET_ALL_REQUEST, {'username': username, 'data': data})
        try:
            stores = super(StoreController, self).get_all(data, db_session, username,
                                                          permission_checked)

            result = [store.to_dict() for store in stores]
            logger.debug(LogMsg.GET_SUCCESS, result)
        except Exception as e:
            logger.exception(LogMsg.GET_FAILED, exc_info=True)
            raise Http_error(404, Message.NOT_FOUND)
        logger.info(LogMsg.END)
        return result

    def get_store_profile(self, id, db_session, username, permission_checked=False):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.MODEL_GETTING)
        model_instance = super(StoreController, self).get(id, db_session, username,
                                                          permission_checked)
        result = model_instance.to_dict()
        logger.debug(LogMsg.GET_SUCCESS, result)
        logger.info(LogMsg.END)

        return result


store_controller = StoreController()
