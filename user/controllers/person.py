import os
from accounts.controller import account_controller
from controller_model import BasicController
from helper import Http_error, Http_response
from log import LogMsg, logger
from messages import Message
from repository.account_repo import delete_person_accounts
from ..models import Person, User
from configs import SIGNUP_USER
from ..constants import PERSON_ADD_SCHEMA_PATH, PERSON_EDIT_SCHEMA_PATH
from ..repository import PersonRepository, UserRepository

save_path = os.environ.get('save_path')

person_schemas = dict(add=PERSON_ADD_SCHEMA_PATH, edit=PERSON_EDIT_SCHEMA_PATH)
person_permissions = dict(add='PERSON_ADD', edit='PERSON_EDIT', get='PERSON_GET',
                          delete='PERSON_DELETE')


class PersonController(BasicController):

    def __init__(self):
        super(PersonController, self).__init__(Person, PersonRepository, person_schemas,
                                               person_permissions)

    def add(self, db_session, data, username, schema_checked=False,
            permission_checked=False):
        logger.info(LogMsg.START, username)

        if username is not None and username == SIGNUP_USER:
            permission_checked = True
        cell_no = data.get('cell_no')
        query_data = dict(filter=dict(cell_no=cell_no))
        if cell_no:
            user_by_cell = super(PersonController, self).get_by_data(query_data,
                                                                     db_session)
            if user_by_cell is not None:
                logger.error(LogMsg.ALREADY_EXISTS, {'cell_no': cell_no})
                raise Http_error(409, Message.ALREADY_EXISTS)

        email = data.get('email')

        if email:
            query_data = dict(filter=dict(email=email))
            user_by_email = super(PersonController, self).get_by_data(query_data,
                                                                      db_session)
            if user_by_email is not None:
                raise Http_error(409, Message.ALREADY_EXISTS)

        model_instance = super(PersonController, self).add(data, db_session, username,
                                                           schema_checked,
                                                           permission_checked)
        account_controller.add_initial_account(model_instance.id, db_session, username)
        logger.info(LogMsg.END)
        return model_instance.to_dict()

    def get(self, id, db_session, username=None, permission_checked=False):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.MODEL_GETTING)
        person = super(PersonController, self).get(id, db_session, username,
                                                   permission_checked)
        return person.to_dict()

    def edit(self, id, db_session, data, username, permission_checked=False):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.EDIT_REQUST, {'person_id': id, 'data': data})
        model_instance = super(PersonController, self).get(id, db_session)

        try:
            super(PersonController, self).edit(id, data, db_session, username,
                                               permission_checked)
            model_instance.full_name = model_instance.set_full_name(model_instance)
            db_session.flush()

            logger.debug(LogMsg.MODEL_ALTERED, model_instance.to_dict())

        except:
            logger.exception(LogMsg.EDIT_FAILED, exc_info=True)
            raise Http_error(500, Message.DELETE_FAILED)

        logger.info(LogMsg.END)
        return model_instance.to_dict()

    def delete(self, id, db_session, username, permission_checked=False):
        logger.info(LogMsg.START, username)

        logger.info(LogMsg.DELETE_REQUEST, {'person_id': id})
        # TODO library def change

        try:
            # TODO accounts
            delete_person_accounts(id, db_session)
            super(PersonController, self).delete(id, db_session, username,
                                                 permission_checked)
            user_repository = UserRepository.generate(User, db_session, username)

            users = user_repository.get_all_by_person(id)
            if users is not None:
                for user in users:
                    db_session.delete(user)

        except Exception as e:
            logger.exception(LogMsg.DELETE_FAILED, exc_info=True)
            raise Http_error(500, Message.DELETE_FAILED)

        logger.info(LogMsg.END)

        return Http_response(204, True)

    def get_all(self, db_session, username, permission_checked=False):
        logger.info(LogMsg.START, username)
        try:
            result = super(PersonController, self).get_all({}, db_session, username,
                                                           permission_checked)
            logger.debug(LogMsg.GET_SUCCESS)
        except:
            logger.error(LogMsg.GET_FAILED)
            raise Http_error(400, LogMsg.GET_FAILED)
        logger.debug(LogMsg.END)
        return result

    def search_person(self, data, db_session, username, permission_checked=False):
        logger.info(LogMsg.START, username)
        logger.debug(LogMsg.GET_ALL_REQUEST, {'username': username, 'data': data})
        try:
            persons = super(PersonController, self).get_all(data, db_session, username,
                                                            permission_checked)

            result = [person.to_dict() for person in persons]
            logger.debug(LogMsg.GET_SUCCESS, result)
        except Exception as e:
            logger.exception(LogMsg.GET_FAILED, exc_info=True)
            raise Http_error(404, Message.NOT_FOUND)
        logger.info(LogMsg.END)
        return result

    def get_person_profile(self, id, db_session, username, permission_checked=False):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.MODEL_GETTING)
        model_instance = super(PersonController, self).get(id, db_session, username,
                                                           permission_checked)
        result = model_instance.to_dict()
        logger.debug(LogMsg.GET_SUCCESS, result)
        logger.info(LogMsg.END)

        return result


person_controller = PersonController()
