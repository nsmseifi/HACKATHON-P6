from check_permission import validate_permissions_and_access
from controller_model import BasicController
from log import logger, LogMsg
from payment.models import CheckoutPressAccount
from user.controllers.user import user_controller
from ..constants import CHECKOUT_ADD_SCHEMA_PATH, CHECKOUT_EDIT_SCHEMA_PATH
from ..repository import CheckoutPressAccountRepository

payment_checkout_schemas = dict(add=CHECKOUT_ADD_SCHEMA_PATH,
                                edit=CHECKOUT_EDIT_SCHEMA_PATH)
payment_checkout_permissions = dict(add='CHECKOUT_PAYMENT_ADD',
                                    edit='CHECKOUT_PAYMENT_EDIT',
                                    get='CHECKOUT_PAYMENT_GET',
                                    delete='CHECKOUT_PAYMENT_DELETE')


class CheckoutPressAccountController(BasicController):

    def __init__(self):
        super(CheckoutPressAccountController, self).__init__(CheckoutPressAccount,
                                                             CheckoutPressAccountRepository,
                                                             payment_checkout_schemas,
                                                             payment_checkout_permissions)

    def exists(self, person_id, db_session):
        query_data = dict(filter=dict(person_id=person_id))
        res = super(CheckoutPressAccountController, self).get_by_data(query_data,
                                                                      db_session)
        return res

    def add_payment(self, data, db_session, username, schema_checked=False,
                    permission_checked=False):
        logger.info(LogMsg.START, username)
        model_instance = super(CheckoutPressAccountController, self).add(data, db_session,
                                                                         username,
                                                                         schema_checked,
                                                                         permission_checked)
        logger.debug(LogMsg.DB_ADD, model_instance.to_dict())
        logger.info(LogMsg.END)
        return model_instance.to_dict()

    def get(self, id, db_session, username, permission_checked=False):
        logger.info(LogMsg.START, username)
        model_instance = super(CheckoutPressAccountController, self).get(id, db_session,
                                                                         username,
                                                                         permission_checked)
        logger.info(LogMsg.END)
        return model_instance.to_dict()

    def internal_get(self, id, db_session):
        return super(CheckoutPressAccountController, self).get(id, db_session)

    def edit(self, id, data, db_session, username, schema_checked=False,
             permission_checked=False):
        logger.info(LogMsg.START, username)
        model_instance = super(CheckoutPressAccountController, self).edit(data,
                                                                          db_session,
                                                                          username,
                                                                          schema_checked,
                                                                          permission_checked)
        logger.debug(LogMsg.EDIT_SUCCESS, model_instance.to_dict())
        logger.info(LogMsg.END)
        return model_instance.to_dict()

    def get_all(self, db_session, data, username):
        logger.info(LogMsg.START, username)
        access_type = validate_permissions_and_access(username, db_session,
                                                      'CHECKOUT_PAYMENT_GET')
        user = user_controller.get_by_username(username, db_session)
        result = super(CheckoutPressAccountController, self).get_all(data, db_session,
                                                                     username)
        final_res = [x.to_dict() for x in result]
        if access_type == 'Press':
            final_res = [x.to_dict() for x in result if x.receiver_id == user.person_id]
        logger.debug(LogMsg.GET_SUCCESS,
                     {'user': user.to_dict(), 'data': final_res,
                      'access_type': access_type})
        logger.debug(LogMsg.END)
        return final_res

    def get_all_paid_for_person(self, person_id, db_session, username):
        logger.info(LogMsg.START, username)
        query_data = dict(filter=dict(reciever_id=person_id))
        result = super(CheckoutPressAccountController, self).get_all_by_data(query_data,
                                                                             db_session,
                                                                             username)
        count = len(result)
        total_paid = 0.0
        final_res = []
        for item in result:
            total_paid += item.amount
            final_res.append(item.to_dict())
        res = {'total_paid': total_paid, 'count': count, 'payment_details': final_res}
        logger.debug(LogMsg.PAYMENT_REPORT_OF_PERSON, res)
        logger.info(LogMsg.END)
        return res


press_payment = CheckoutPressAccountController()
