from uuid import uuid4

from controller_model import BasicController
from infrastructure.schema_validator import schema_validate
from log import LogMsg, logger
from helper import Now, Http_error, value
from messages import Message
from .models import APP_Token
from .constants import ADD_SCHEMA_PATH
from .repository import TokenRepository

token_expiration_interval = value('token_expiration_interval', '1200')
new_token_request_valid_interval = value('new_token_request_valid_interval', '30')

schemas = dict(add=ADD_SCHEMA_PATH)


class TokenController(BasicController):
    def __init__(self):
        super(TokenController, self).__init__(APP_Token, TokenRepository, schemas,
                                              None)

    def current_token(self, db_session, username):
        query_data = dict(filter=dict(username=username, expiration_date={'$gte': Now()}))
        res = super(TokenController, self).get_by_data(query_data, db_session)
        return res

    def add(self, db_session, data, username):
        logger.info(LogMsg.START, username)
        schema_validate(data, ADD_SCHEMA_PATH)

        logger.debug(LogMsg.CHECKING_VALID_TOKEN, username)
        current_token = self.current_token(db_session, username)
        if current_token is not None and \
                current_token.expiration_date > Now():
            logger.debug(LogMsg.USER_HAS_VALID_TOKEN, current_token.id)
            return current_token.to_dict()
        data = dict(expiration_date=Now() + int(token_expiration_interval),
                    username=username)
        res = super(TokenController, self).add(data, db_session, username, True)
        logger.debug(LogMsg.TOKEN_CREATED)

        logger.info(LogMsg.END)
        return res.to_dict()

    def get(self, id, db_session, username):
        logger.info(LogMsg.START, username)
        res = super(TokenController, self).get(id, db_session, username)
        if res is None:
            logger.error(LogMsg.MODEL_GETTING_FAILED)
            raise Http_error(404, Message.TOKEN_INVALID)
        if res.expiration_date < Now():
            logger.error(LogMsg.TOKEN_EXPIRED)
            raise Http_error(401, Message.TOKEN_EXPIRED)

        logger.info(LogMsg.END)
        return res.to_dict()


token = TokenController()
