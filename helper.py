import datetime
from os import environ
import time
from base64 import b64encode, b64decode
from bottle import request, HTTPResponse
from log import LogMsg, logger
from app_token.models import APP_Token
from messages import Message
from user.models import User
from db_session import Session
import json


# AUTHORIZATION ACTIONS

def validate_token(id, db_session):
    result = db_session.query(APP_Token).filter(APP_Token.id == id).first()
    if result is None or result.expiration_date < Now():
        raise Http_error(401, Message.TOKEN_INVALID)
    return result


def if_login(func):
    def wrapper(*args, **kwargs):
        logger.debug(LogMsg.AUTH_CHECKING)

        kwargs['username'] = check_login()['username']

        logger.debug(LogMsg.AUTH_SUCCEED)
        logger.debug("user is {}".format(kwargs['username']))

        rtn = func(*args, **kwargs)
        return rtn

    return wrapper


def check_login():
    db_session = get_db_session()
    auth = request.get_header('Authorization')
    if auth is None:
        return {'username': None}

    username, password = decode(auth)

    if password is None:
        return model_to_dict(validate_token(username, db_session))

    else:
        user = db_session.query(User).filter(User.username == username,
                                             User.password == password).first()

        if user is None:
            return {'username': None}
        return model_to_dict(user)


def check_Authorization():
    db_session = get_db_session()
    auth = request.get_header('Authorization')
    if auth is None:
        raise Http_error(401, Message.NO_AUTH)

    username, password = decode(auth)

    if password is None:
        return model_to_dict(validate_token(username, db_session))

    else:
        user = db_session.query(User).filter(User.username == username,
                                             User.password == password).first()

        if user is None:
            raise Http_error(401, Message.INVALID_USERNAME)
        return model_to_dict(user)



def check_unrequired_Authorization():
    db_session = get_db_session()
    auth = request.get_header('Authorization')
    if auth is None:
        return {'username':None}
    username, password = decode(auth)

    if password is None:
        return model_to_dict(validate_token(username, db_session))

    else:
        user = db_session.query(User).filter(User.username == username,
                                             User.password == password).first()

        if user is None:
            return {'username':None}
        return model_to_dict(user)


def encode(username, password):
    """Returns an HTTP basic authentication encrypted string given a valid
    username and password.
    """
    if ':' in username:
        raise Http_error(400, "username has not valid schema")

    username_password = '%s:%s' % (str(username), str(password))
    return 'Basic ' + b64encode(username_password.encode()).decode()


def decode(encoded_str):
    """Decode an encrypted HTTP basic authentication string. Returns a tuple of
    the form (username, password), and raises a DecodeError exception if
    nothing could be decoded.
    """
    split = encoded_str.strip().split(' ')

    # If split is only one element, try to decode the username and password
    # directly.
    if len(split) == 1:
        try:
            username, password = b64decode(split[0]).decode().split(':', 1)
        except:
            raise Http_error(400, Message.AUTH_DECODING_FAILED)

    # If there are only two elements, check the first and ensure it says
    # 'basic' so that we know we're about to decode the right thing. If not,
    # bail out.
    elif len(split) == 2:
        if split[0].strip().lower() == 'basic':
            logger.debug("auth is basic")
            try:
                username, password = b64decode(split[1]).decode().split(':', 1)
            except:
                raise Http_error(400, Message.AUTH_DECODING_FAILED)

        elif split[0].strip().lower() == 'bearer':
            logger.debug("auth is bearer")
            username, password = split[1].strip(), None
            logger.debug(
                "token is {} and pass is {}".format(username, password))
        else:
            raise Http_error(400, Message.AUTH_DECODING_FAILED)

    # If there are more than 2 elements, something crazy must be happening.
    # Bail.
    else:
        raise Http_error(400, Message.AUTH_DECODING_FAILED)

    if password is None:
        return str(username), password

    return str(username), str(password)


# DECORATORS

def check_auth(func):
    def wrapper(*args, **kwargs):
        logger.debug(LogMsg.AUTH_CHECKING)

        kwargs['username'] = check_Authorization()['username']

        logger.debug(LogMsg.AUTH_SUCCEED)
        logger.debug("user is {}".format(kwargs['username']))

        rtn = func(*args, **kwargs)
        return rtn

    return wrapper

def check_unrequirde_auth(func):
    def wrapper(*args, **kwargs):
        logger.debug(LogMsg.AUTH_CHECKING)

        kwargs['username'] = check_unrequired_Authorization()['username']

        logger.debug(LogMsg.AUTH_SUCCEED)
        logger.debug("user is {}".format(kwargs['username']))

        rtn = func(*args, **kwargs)
        return rtn

    return wrapper


def get_db_session():
    if hasattr(request, 'db_session'):
        return request.db_session
    else:
        request.db_session = Session()
        return request.db_session


def inject_db(func):
    def wrapper(*args, **kwargs):
        kwargs['db_session'] = get_db_session()

        # generate_RID()
        rtn = func(*args, **kwargs)
        db_session = kwargs['db_session']
        try:
            db_session.commit()
        except Exception as e:

            logger.exception(LogMsg.COMMIT_ERROR, exc_info=True)

            raise Http_error(500, Message.COMMIT_FAILED)
        return rtn

    return wrapper


def jsonify(func):
    def wrapper(*args, **kwargs):
        rtn = func(*args, **kwargs)
        result = None
        if isinstance(rtn, list):
            result = []
            for item in rtn:
                if isinstance(item, str):
                    result.append(item)
                else:
                    result.append(model_to_dict(item))
            result = {"result": result}
        else:
            result = model_to_dict(rtn)
        return result

    return wrapper


def pass_data(func):
    def wrapper(*args, **kwargs):
        if request.json is not None:
            kwargs['data'] = request.json
        elif request.forms is not None:
            my_data={}
            data_list = request.forms.dict

            if request.query and request.query.dict:
                data_list.update(request.query.dict.copy())

            for key in data_list.keys():
                my_data[key] = data_list[key][0]

            if (request.files != None) and (request.files.dict != None):
                my_data['files'] = request.files.dict.get('files')

            kwargs['data'] = my_data

        rtn = func(*args, **kwargs)
        return rtn

    return wrapper


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        finish_time = time.time()

        logger.info(str({'duration': finish_time - start_time}))

        if finish_time - start_time > 1:
            logger.warning(
                'request lasted long for {}'.format(finish_time - start_time))

        return result

    return wrapper


# TIME FUNCS
def Now():
    now = time.mktime(datetime.datetime.now().timetuple())
    return int(now)


# HTTP RESPONSE HANDLERS
def Http_error(code, message):
    if isinstance(message, str):
        message = {'msg': message}
    result = HTTPResponse(body=json.dumps(message), status=code,
                          headers={'Content-type': 'application/json'})
    return result


def Http_response(code, message):
    if isinstance(message, str):
        message = {'msg': message}
    result = HTTPResponse(body=json.dumps(message), status=code,
                          headers={'Content-type': 'application/json'})
    return result


def value(name, default):
    return environ.get(name) or default


# MODEL DATA HANDLING FUNCS
def check_schema(required_list, data_keys):
    required = set(required_list)
    keys = set(data_keys)

    result = required.issubset(keys)

    if result == False:
        raise Http_error(400, Message.MISSING_REQUIERED_FIELD)

    return result

def model_basic_dict(model_instance):
    result = {

        'creation_date': model_instance.creation_date,
        'creator': model_instance.creator,
        'id': model_instance.id,
        'modification_date': model_instance.modification_date,
        'modifier': model_instance.modifier,
        'version': model_instance.version,
        'tags': model_instance.tags
    }
    return result


def model_to_dict(obj):
    object_dict = obj
    if not isinstance(obj,dict):
        object_dict = dict((name, getattr(obj, name)) for name in dir(obj) if
                           callable(getattr(obj,name))==False and
                           name.startswith('_')==False)
                           #
                           # (not name.startswith('_')) and not name.startswith(
                           #         'to_dict')and not name.startswith(
                           #         'edit')and not name.startswith(
                           #         'get_by_id')and not name.startswith(
                           #         'populate_data')and not name.startswith(
                           #         'edit_basic_data')and not name.startswith(
                           #     'mongo') and not name.startswith(
                           #     'create_query')) if not isinstance(obj,
                           #                                        dict) else obj

    if "metadata" in object_dict:
        del object_dict['metadata']
    return object_dict


def multi_model_to_dict(obj_list):
    result = []
    for item in obj_list:
        obj = model_to_dict(item)
        result.append(obj)
    return result


