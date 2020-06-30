from accounts.models import Account
from controller_model import BasicController
from enums import  AccountTypes
from financial_transactions.controller import transaction_controller
from helper import Http_error, Http_response
from log import LogMsg
from messages import Message

from log import logger

from user.models import Person, User
from user.repository import PersonRepository, UserRepository
from .constants import ADD_SCHEMA_PATH, EDIT_SCHEMA_PATH
from .repository import AccountRepository

account_schemas = dict(add=ADD_SCHEMA_PATH, edit=EDIT_SCHEMA_PATH)
account_permissions = dict(add='ACCOUNT_ADD', edit='ACCOUNT_EDIT', get='ACCOUNT_GET',
                           delete='ACCOUNT_DELETE')


class AccountController(BasicController):

    def __init__(self):
        super(AccountController, self).__init__(Account, AccountRepository,
                                                account_schemas,
                                                account_permissions)

    def exists(self, type, person_id, db_session):
        query_data = dict(filter=dict(type=type, person_id=person_id))
        res = super(AccountController, self).get_by_data(query_data, db_session)
        return res

    def add(self, data, db_session, username, schema_checked=False,
            permission_checked=False,transaction_added=False):
        logger.debug(LogMsg.START, username)
        type = data.get('type', None)
        if type is None:
            data['type'] = 'Main'
        person_id = data.get('person_id')
        person_repository = PersonRepository.generate(Person, db_session, username)
        person = person_repository.get_by_id(person_id)
        if person is None:
            logger.error(LogMsg.NOT_FOUND, {'person_id': person_id})
            raise Http_error(404, Message.NOT_FOUND)


        account = self.exists(data.get('type'), person_id, db_session)
        if account is not None:
            raise Http_error(409, Message.ALREADY_EXISTS)

        account = super(AccountController, self).add(data, db_session, username,
                                                     schema_checked,
                                                     permission_checked)
        logger.debug(LogMsg.DB_ADD, account.to_dict())
        logger.info(LogMsg.END)
        return account.to_dict()

    def get(self, person_id, type, db_session,username=None, schema_checked=False,
            permission_checked=False):
        logger.info(LogMsg.START)
        data = dict(filter=dict(person_id=person_id, type=type))
        try:
            result = super(AccountController, self).get_by_data(data, db_session,
                                                                username,
                                                                schema_checked,
                                                                permission_checked)
        except Exception as e:
            logger.error(LogMsg.GET_FAILED,
                         {'person_id': person_id, 'account_type': type},
                         exc_info=True)
            raise Http_error(404, Message.GET_FAILED)

        logger.info(LogMsg.END)

        return result

    def get_person_accounts(self, person_id, db_session, username,
                            permission_checked=False):
        logger.info(LogMsg.START, username)
        data = dict(filter=dict(person_id=person_id))
        result = super(AccountController, self).get_all_by_data(data, db_session,
                                                                username,
                                                                permission_checked)
        rtn = [item.to_dict() for item in result]
        logger.debug(LogMsg.GET_SUCCESS, rtn)
        logger.info(LogMsg.END)
        return rtn

    def get_all(self, data, db_session, username, schema_checked=False,
                permission_checked=False):
        logger.info(LogMsg.START, username)
        res = super(AccountController, self).get_all(data, db_session, username,
                                                     permission_checked)
        result = [account.to_dict() for account in res]
        logger.info(LogMsg.END)
        return result

    def get_user_accounts(self, username, db_session, data, schema_checked=False,
                          permission_checked=False):
        logger.info(LogMsg.START, username)
        user_repository = UserRepository.generate(User, db_session, username)
        user = user_repository.get_by_username(username)
        if user is None:
            logger.error(LogMsg.NOT_FOUND, username)
            raise Http_error(404, Message.INVALID_USER)

        if data.get('filter') is None:
            data.update({'filter': {'person_id': user.person_id}})
        else:
            data['filter'].update({'person_id': user.person_id})
        return self.get_all(data, db_session, username, schema_checked,
                            permission_checked)

    def delete_all(self, username, db_session, schema_checked=False,
                   permission_checked=False):
        logger.info(LogMsg.START, username)
        user_repository = UserRepository.generate(User, db_session, username)
        user = user_repository.get_by_username(username)
        if user is None:
            logger.error(LogMsg.NOT_FOUND, username)
            raise Http_error(404, Message.INVALID_USER)
        data = dict(filter=dict(person_id=user.person_id))
        super(AccountController, self).delete_all_by_data(data, db_session, username,
                                                          schema_checked,
                                                          permission_checked)
        logger.info(LogMsg.END)
        return Http_response(204, True)

    def edit_account_value(self, account_id, value, db_session, username=None,
                           schema_checked=False,
                           permission_checked=False):
        logger.info(LogMsg.START)
        account = super(AccountController, self).get(account_id, db_session, username,
                                                     schema_checked,
                                                     permission_checked)
        if account is None:
            logger.error(LogMsg.NOT_FOUND, {'account_id': account_id})
            raise Http_error(404, Message.NOT_FOUND)
        account.value += value
        transaction_data = {'account_id': account_id}
        if value>0:
            transaction_data.update({'credit':value})
        else:
            transaction_data.update({'debit':value})
        transaction_controller.internal_add(transaction_data,db_session)
        logger.info(LogMsg.END)

        return account.to_dict()

    def get_by_id(self, id, db_session, username, schema_checked=False,
                  permission_checked=False):
        logger.info(LogMsg.START, username)
        account = super(AccountController, self).get(id, db_session, username,
                                                     permission_checked)
        logger.info(LogMsg.END)
        return account.to_dict()

    def edit(self, id, data, db_session, username, schema_checked=False,
             permission_checked=False):
        logger.info(LogMsg.START, username)
        account = super(AccountController, self).edit(id, data, db_session, username,
                                                      schema_checked, permission_checked)
        logger.info(LogMsg.END)
        return account.to_dict()

    def add_initial_account(self, person_id, db_session, username=None):
        logger.info(LogMsg.START, username)
        data = {'person_id': person_id, 'value': 0.0, 'type': 'Main'}
        account = super(AccountController, self).add(data, db_session, username,
                                                     permission_checked=True)
        logger.info(LogMsg.END)

        return account.to_dict()

    def edit_by_person(self, data, db_session, username):
        logger.info(LogMsg.START, username)
        value = data.get('value')
        data.pop('value')
        if data.get('type') is None:
            data['filter']['type'] = 'Main'
        account = super(AccountController, self).get_by_data(data, db_session, username)
        logger.debug(LogMsg.GETTING_ACCOUNT_PERSON, data)
        if account is None:
            logger.error(LogMsg.NOT_FOUND, {'account_id': account.id})
            raise Http_error(404, Message.NOT_FOUND)
        account.value += value
        transaction_data = {'account_id': account.id}
        if value > 0:
            transaction_data.update({'credit': value})
        else:
            transaction_data.update({'debit': value})
        transaction_controller.internal_add(transaction_data, db_session)

        logger.info(LogMsg.END)
        return account.to_dict()

    def profile_account_info(self, person_id, db_session, username):
        result = self.get_person_accounts(person_id, db_session, username, True)
        for item in result:
            del item['person_id']
            del item['person']
        return result


account_controller = AccountController()
