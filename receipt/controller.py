import os
import pyqrcode
from random import randint
from controller_model import BasicController
from helper import Http_error, Http_response
from log import LogMsg, logger
from messages import Message
from .models import Store
from .constants import ADD_SCHEMA_PATH
from .repository import StoreRepository

save_path = os.environ.get('save_path')

store_schemas = dict(add=ADD_SCHEMA_PATH)

class ReceiptController(BasicController):

    def __init__(self):
        super(ReceiptController, self).__init__(Store, StoreRepository, store_schemas)

    def add(self, db_session, data, username):
        logger.info(LogMsg.START, username)
        
        model_instance = super(ReceiptController, self).add(data, db_session, username)
        logger.info(LogMsg.END)
        return model_instance.to_dict()

    def get(self, id, db_session, username=None):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.MODEL_GETTING)
        store = super(ReceiptController, self).get(id, db_session, username)
        return store.to_dict()

    def edit(self, id, db_session, data, username, permission_checked=False):
        logger.info(LogMsg.START, username)

        model_instance = super(ReceiptController, self).get(id, db_session)
        if 'id' in data:
            del data['id']
        try:
            super(ReceiptController, self).edit(id, data, db_session, username,
                                               permission_checked)

            logger.debug(LogMsg.MODEL_ALTERED, model_instance.to_dict())

        except:
            logger.exception(LogMsg.EDIT_FAILED, exc_info=True)
            raise Http_error(500, Message.DELETE_FAILED)

        logger.info(LogMsg.END)
        return model_instance.to_dict()

    def delete(self, id, db_session, username, permission_checked=False):
        logger.info(LogMsg.START, username)
        try:
            super(ReceiptController, self).delete(id, db_session, username,
                                                 permission_checked)

        except Exception as e:
            logger.exception(LogMsg.DELETE_FAILED, exc_info=True)
            raise Http_error(500, Message.DELETE_FAILED)

        logger.info(LogMsg.END)

        return Http_response(204, True)

    def get_all(self, db_session, username, permission_checked=False):
        logger.info(LogMsg.START, username)
        try:
            result = super(ReceiptController, self).get_all({}, db_session, username,
                                                           permission_checked)
            logger.debug(LogMsg.GET_SUCCESS)
        except:
            logger.error(LogMsg.GET_FAILED)
            raise Http_error(400, LogMsg.GET_FAILED)
        logger.debug(LogMsg.END)
        return result

    def generate_QR(self,url_str):
        url = pyqrcode.create(url_str)
        url.svg('Receipt_QR_{}.svg'.format(randint(100000,999999)), scale=8)
        url.eps('Receipt_QR.eps', scale=2)
        return url.terminal(quiet_zone=1)

    
receipt_controller = ReceiptController()
