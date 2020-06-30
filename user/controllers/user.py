from accounts.controller import account_controller

from controller_model import BasicController
from enums import Permissions
from log import LogMsg, logger
from helper import Http_error
from messages import Message
from user.models import User
from ..constants import USER_ADD_SCHEMA_PATH, USER_EDIT_SCHEMA_PATH
from ..repository import UserRepository
from .person import person_controller

user_schemas = dict(add=USER_ADD_SCHEMA_PATH, edit=USER_EDIT_SCHEMA_PATH)
user_permissions = dict(edit='USER_EDIT', get='USER_GET',
                        delete='USER_DELETE')


class UserController(BasicController):

    def __init__(self):
        super(UserController, self).__init__(User, UserRepository, user_schemas,
                                             user_permissions)

    def add(self, db_session, data, username, schema_checked=False,
            permission_checked=False):
        new_username = data.get('username')
        query_data = dict(filter=dict(username=new_username))
        user = super(UserController, self).get_by_data(query_data, db_session)
        if user is not None:
            logger.error(LogMsg.USER_XISTS, new_username)
            raise Http_error(409, Message.USERNAME_EXISTS)
        person_id = data.get('person_id')
        if person_id is None:
            raise Http_error(404, Message.NOT_FOUND)
        # TODO validate_person must be changed

        user = super(UserController, self).add(data, db_session, username)
        logger.debug(LogMsg.DB_ADD, user.to_dict())
        logger.info(LogMsg.END)

        return user.to_dict()

    def get_by_person(self, person_id, db_session):
        query_data = dict(filter=dict(person_id=person_id))
        return super(UserController, self).get_by_data(query_data, db_session)

    def get_by_username(self, username, db_session):
        query_data = dict(filter=dict(username=username))
        return super(UserController, self).get_by_data(query_data, db_session)

    def get(self, id, db_session, username):
        logger.info(LogMsg.START, username)
        logger.debug(LogMsg.MODEL_GETTING, {'user_id': id})
        model_instance = super(UserController, self).get(id, db_session, username, True)
        if model_instance:
            result = model_instance.to_dict()
            logger.debug(LogMsg.GET_SUCCESS, result)
        else:
            logger.debug(LogMsg.NOT_FOUND, {'user_id': id})
            raise Http_error(404, Message.NOT_FOUND)
        logger.info(LogMsg.END)
        return result

    def get_profile(self, username, db_session):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.MODEL_GETTING, {'user.username': username})
        query_data = dict(filter=dict(username=username))
        user = super(UserController, self).get_by_data(query_data, db_session,
                                                       username,
                                                       permission_checked=True)
        if user is None:
            logger.debug(LogMsg.NOT_FOUND, {'user.username': username})
            raise Http_error(404, Message.NOT_FOUND)
        result = user.to_dict()
        result['account_info'] = account_controller.profile_account_info(user.person_id,
                                                                         db_session,
                                                                         username) or None
        logger.info(LogMsg.END)

        return result

    def delete(self, id, db_session, username):
        logger.info(LogMsg.START, username)
        logger.debug(LogMsg.DELETE_REQUEST, {'user_id': id})

        try:
            super(UserController, self).delete(id, db_session, username)
            logger.debug(LogMsg.DELETE_SUCCESS, {'user_id': id})
        except:
            logger.exception(LogMsg.DELETE_FAILED, exc_info=True)
            raise Http_error(404, LogMsg.DELETE_FAILED)
        logger.info(LogMsg.END)
        return {}

    def get_all(self, db_session, username):
        logger.info(LogMsg.START, username)
        logger.debug(LogMsg.GET_ALL_REQUEST)
        result = super(UserController, self).get_all({}, db_session, username)
        final_res = [item.to_dict() for item in result]

        logger.debug(LogMsg.GET_SUCCESS, final_res)
        logger.info(LogMsg.END)

        return final_res

    def search_user(self, data, db_session, username):
        logger.info(LogMsg.START, username)
        result = super(UserController, self).get_all(data, db_session, username)
        final_res = [item.to_dict() for item in result]
        logger.debug(LogMsg.GET_SUCCESS, final_res)
        logger.info(LogMsg.END)

        return final_res

    def edit(self, id, db_session, data, username):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.EDIT_REQUST, {'user_id': id, 'data': data})

        result = super(UserController, self).edit(id, data, db_session, username)

        logger.debug(LogMsg.EDIT_SUCCESS, result.to_dict())
        logger.info(LogMsg.END)

        return result.to_dict()

    def edit_profile(self, id, db_session, data, username):
        logger.info(LogMsg.START, username)

        logger.debug(LogMsg.EDIT_REQUST, data)

        user = self.get(id, db_session, username)
        if user:
            logger.debug(LogMsg.MODEL_GETTING, {'user_id': id})
            if user.person_id:
                person = user.person
                if person:
                    person_controller.edit(person.id, db_session, data, username,
                                           permission_checked=True)
                else:
                    raise Http_error(404, LogMsg.NOT_FOUND)
            else:
                person = person_controller.add(db_session, data,
                                               username, permission_checked=True)
                user.person_id = person.id
        else:
            logger.debug(LogMsg.NOT_FOUND, {'user_id': id})
            raise Http_error(404, Message.NOT_FOUND)

        user_dict = user.to_dict()
        logger.debug(LogMsg.MODEL_ALTERED, user_dict)
        logger.info(LogMsg.END)

        return user_dict


user_controller = UserController()
