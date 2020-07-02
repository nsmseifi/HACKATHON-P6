import json
from configs import SIGNUP_USER
from helper import Http_error
from log import logger, LogMsg
from app_redis import app_redis as redis
from messages import Message
from store.controller import store_controller

from user.controllers.user import user_controller
from user.controllers.person import person_controller
from infrastructure.schema_validator import schema_validate
from .constants import SIGN_UP_SCHEMA_PATH

def signup(data, db_session, *args, **kwargs):
    logger.info(LogMsg.START, data)
    schema_validate(data, SIGN_UP_SCHEMA_PATH)
    user_data = {k: v for k, v in data.items() if k in ['username', 'password']}
    person_data = {k: v for k, v in data.items() if k not in user_data.keys()}

    person = person_controller.add(db_session, person_data, SIGNUP_USER,permission_checked=True)

    if user_data:
        user_data.update({'person_id': person.get('id')})
    user = user_controller.add(db_session, user_data, SIGNUP_USER, False, True)
    logger.info(LogMsg.END)
    return user

def signup_store(data, db_session, *args, **kwargs):
    logger.info(LogMsg.START, data)
    schema_validate(data, SIGN_UP_SCHEMA_PATH)
    user_data = {k: v for k, v in data.items() if k in ['username', 'password']}
    person_data = {k: v for k, v in data.items() if k not in user_data.keys()}

    person = person_controller.add(db_session, person_data, SIGNUP_USER,permission_checked=True)

    if user_data:
        user_data.update({'person_id': person.get('id')})
    person_data.update({'id':person.get('id')})
    store = store_controller.add(db_session,person_data)
    user = user_controller.add(db_session, user_data, SIGNUP_USER, False, True)
    user['store'] = store
    logger.info(LogMsg.END)
    return user
