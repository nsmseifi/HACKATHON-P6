from controller_model import BasicController
from financial_transactions.models import Transaction
from helper import Http_error
from log import LogMsg, logger
from messages import Message
from repository.account_repo import get_account
from .constants import ADD_SCHEMA_PATH
from .repository import TransactionRepository

transaction_schemas = dict(add=ADD_SCHEMA_PATH)
transaction_permissions = dict(add='TRANSACTION_ADD', get='TRANSACTION_GET',
                               delete='TRANSACTION_DELETE')


class TransactionController(BasicController):

    def __init__(self):
        super(TransactionController, self).__init__(Transaction, TransactionRepository,
                                                    transaction_schemas,
                                                    transaction_permissions)

    def exists(self, keyName, db_session):
        query_data = dict(filter=dict(keyName=keyName))
        res = super(TransactionController, self).get_by_data(query_data, db_session)
        if res is None:
            return False
        return res

    def add(self, data, db_session, username=None):
        logger.info(LogMsg.START, username)

        account_id = data.get('account_id')
        logger.debug(LogMsg.GETTING_ACCOUNT_BY_ID, account_id)
        account = get_account(account_id, db_session)
        if account is None:
            logger.error(LogMsg.NOT_FOUND, {'account_id': account_id})
            raise Http_error(404, Message.NOT_FOUND)

        model_instance = super(TransactionController, self).add(data, db_session,
                                                                username)
        logger.debug(LogMsg.TRANSACTION_ADDED, model_instance.to_dict())
        logger.info(LogMsg.END)

        return model_instance.to_dict()

    def get(self, id, db_session, username=None):
        logger.info(LogMsg.START, username)

        model_instance = super(TransactionController, self).get(id, db_session, username)
        if model_instance is None:
            logger.error(LogMsg.NOT_FOUND, {'transaction_id': id})
            raise Http_error(404, Message.NOT_FOUND)
        return model_instance.to_dict()

    def get_all(self, data, db_session, username):
        logger.info(LogMsg.START, username)

        result = super(TransactionController, self).get_all(data, db_session, username)
        res = [item.to_dict() for item in result]
        logger.info(LogMsg.END)
        return res

    def internal_add(self, data, db_session):
        logger.info(LogMsg.START)

        model_instance = super(TransactionController, self).add(data, db_session,
                                                                schema_checked=True,
                                                                permission_checked=True)

        logger.info(LogMsg.END)

        return model_instance.to_dict()


transaction_controller = TransactionController()
