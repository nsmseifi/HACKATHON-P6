import os
import pyqrcode
from random import randint
from financial_transactions.controller import transaction_controller as transaction
from accounts.controller import account_controller
from controller_model import BasicController
from file_handler.handle_file import return_file
from helper import Http_error, Http_response
from log import LogMsg, logger
from messages import Message
from repository.user_repo import check_user
from .models import Receipt
from .constants import ADD_SCHEMA_PATH
from .repository import ReceiptRepository

save_path = os.environ.get('save_path')

receipt_schemas = dict(add=ADD_SCHEMA_PATH)

class ReceiptController(BasicController):

    def __init__(self):
        super(ReceiptController, self).__init__(Receipt, ReceiptRepository, receipt_schemas)

    def add(self, db_session, data, username=None):
        logger.info(LogMsg.START, username)
        data['status']='Waiting'
        
        model_instance = super(ReceiptController, self).add(data, db_session, username)
        logger.info(LogMsg.END)
        result = self.generate_QR(model_instance.id)
        return return_file(result)

    def get(self, id, db_session, username=None):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.MODEL_GETTING)
        receipt = super(ReceiptController, self).get(id, db_session, username)
        return receipt.to_dict()
    def internal_get(self, id, db_session, username=None):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.MODEL_GETTING)
        receipt = super(ReceiptController, self).get(id, db_session, username)
        return receipt

    def edit(self, id, db_session, data, username=None, permission_checked=False):
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

    def delete(self, id, db_session, username=None, permission_checked=False):
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

    def pay(self,id,db_session,username=None):
        logger.info(LogMsg.START,username)
        receipt = self.internal_get(id,db_session,username)
        if receipt is None:
            raise Http_error(404,Message.NOT_FOUND)

        if username is None:
        #       paypal pay
            pass
        else:
            user = check_user(username,db_session)
            receipt.payer_id = user.person_id

            account = account_controller.get(user.person_id, 'Main',db_session)
            if account is None:
                logger.error(LogMsg.NOT_FOUND,
                             {'person_id': user.person_id})
                raise Http_error(404, Message.USER_HAS_NO_ACCOUNT)

            if account.value < receipt.total_payment:
            #     paypal pay
                pass
            else:
                account.value -= receipt.total_payment

            transaction_data = {'account_id': account.id, 'debit': receipt.total_payment}
            transaction.internal_add(transaction_data, db_session)

        receipt.status = 'Paid'
        return receipt.to_dict()

    def user_receipts(self,db_session,username):
        logger.info(LogMsg.START,username)
        user = check_user(username,db_session)
        data = dict(filter=dict(payer_id=user.person_id))
        return self.get_all_by_data(data,db_session,username)

    def store_receipts(self,db_session,store_id,username=None):
        logger.info(LogMsg.START,store_id)
        data = dict(filter=dict(payee_id=store_id))
        return self.get_all_by_data(data, db_session)

    def generate_QR(self,receipt_id):
            url_str = 'https://drep.xyz/statics/show-receipt/{}'.format(receipt_id)
            url = pyqrcode.create(url_str)
            filename = 'Receipt_QR_{}.png'.format(randint(100000,999999))
            url.png('{}/{}'.format(save_path,filename), scale=6, module_color=[0, 0, 0, 128],
                         background=[0xff, 0xff, 0xcc])

            return filename

    
receipt_controller = ReceiptController()
