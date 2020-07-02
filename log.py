import os
import gzip
import logging.handlers
import logging.config

from bottle import request

log_file = os.environ.get('log_path')
print('log_file : {}'.format(log_file))


def create_version_conflict_details(obj_version, request_version):
    return {'object version': obj_version, 'request version': request_version}


def create_security_details(obj_domain_id, obj_security_tags):
    return {'object domain id': obj_domain_id,
            'object security tags': obj_security_tags}


def create_can_not_be_deleted_details(obj_id, error_msg):
    return {'id': obj_id, 'sql error': error_msg}


def get_request_id():
    try:
        if hasattr(request, 'JJP_RID'):
            return request.JJP_RID
    except RuntimeError:
        return 'NO_RID'


class GZipRotator:
    def __call__(self, source, dest):
        os.rename(source, dest)
        f_in = open(dest, 'rb')
        f_out = gzip.open("%s.gz" % dest, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(dest)


class JJPFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(JJPFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(JJPFormatter, self).format(record)
        s = "{} - {}".format(get_request_id(), s)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s


handler = logging.handlers.TimedRotatingFileHandler(filename=log_file,
                                                    encoding='utf8',
                                                    when='Midnight',
                                                    interval=1,backupCount=5)

logger = logging.getLogger(__name__)
fmtr = JJPFormatter(
    '%(asctime)s,%(msecs)d %(levelname)-2s[%(pathname)s :%(lineno)d - %(funcName)s] %(message)s')

handler.setFormatter(fmtr)
logger.addHandler(handler)
logging.basicConfig(
    filename=log_file,
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)


class LogMsg:
    COMMIT_ERROR="Commit Error"
    START = "function is called -- user is : %s "
    END = "function finished successfully "
    ADDING_ERR = "adding model to database encountered a problem  "
    DATETIME_ADDITION = "date time added to model  "
    INSTANCE_POPULATED = "instance populated with data and ready to add to db : %s"
    DATA_ADDITION = "data added to model : %s "
    DB_ADD = "model added to database : %s  "
    AUTH_CHECKING = "going to check authentication  "
    AUTH_SUCCEED = "authentication is successful  "
    GET_SUCCESS = "getting from database is successful : %s "
    GET_FAILED = "getting from database failed : %s "
    DELETE_SUCCESS = "deleting item is done successfully  "
    DELETE_FAILED = "deleting the item encountered a problem "
    DELETE_REQUEST = "request for deleting item : %s"
    EDIT_REQUST = "editing the item : %s"
    ALREADY_EXISTS = "entity by this data already exists : %s"
    VERSION_CONFLICT = "version of requesting data is not same as model"
    EDIT_SUCCESS = "editing item is done successfully  "
    EDIT_FAILED = "editing the item encountered a problem  "
    MODEL_GETTING = "model_instance getting from database by id : %s "
    MODEL_GETTING_FAILED = "item is not exists in database  "
    MODEL_ALTERED = "item altered successfully : %s "
    GET_ALL_REQUEST = "getting all request from db..."
    NOT_FOUND = "no such item exists : %s"
    COMMIT_FAILED = 'commiting process failed'
    TOKEN_CREATED = 'a new token for user created'
    TOKEN_EXPIRED = 'token is expired'
    TOKEN_DELETED = 'token deleted successfuly'
    TOKEN_INVALID = 'token is invalid'
    ALTERING_AUTHORITY_FAILED = 'user has no admission to alter the item'
    DELETE_PROCESSING = 'going to delete the item from db'
    GATHERING_RELATIVES = 'gathering item reletives to delete them from db'
    DELETE_RELATIVE = 'the reletive %s is going to be delete'
    UPLOAD_NOT_ALLOWED = 'no more uploads supports in edit'
    USER_XISTS = 'user by this username : %s already exists'
    CHECK_REDIS_FOR_EXISTANCE = 'checking redis if cell number already ' \
                                'exists...'
    INVALID_ENTITY_TYPE = 'the entity type is invalid : %s'
    REGISTER_XISTS = 'user has already valid registery code'
    CHECK_USER_EXISTANCE = 'checking user if already exists'
    DATA_MISSING = 'required data doesnt exists in data : %s'
    SCHEMA_NOT_VALID = 'SCHEMA_NOT_VALID'
    LOW_BALANCE = 'low balance in account'
