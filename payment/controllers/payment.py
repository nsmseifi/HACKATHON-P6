from controller_model import BasicController
from log import logger, LogMsg
from payment.models import Payment
from payment.repository import PaymentRepository

payment_permissions = dict(add='ACCOUNT_ADD', get='ACCOUNT_GET')


class PaymentController(BasicController):

    def __init__(self):
        super(PaymentController, self).__init__(Payment, PaymentRepository,
                                                None,
                                                payment_permissions)

    def exists(self, person_id, db_session):
        query_data = dict(filter=dict(person_id=person_id))
        res = super(PaymentController, self).get_by_data(query_data, db_session)
        return res

    def add_payment(self, data, db_session, username):
        logger.info(LogMsg.START, username)
        data['used'] = False
        data['status'] = 'SendToBank'
        if data['details'] is None:
            data['details'] = dict()
        data['details'].update({'call_back_url': data.get('call_back_url')})
        model_instance = super(PaymentController, self).add(data, db_session, username,permission_checked=True)
        logger.debug(LogMsg.PAYMENT_ADDED, model_instance.to_dict())
        logger.info(LogMsg.END)
        return model_instance.to_dict()

    def get(self, shopping_id, db_session):
        logger.info(LogMsg.START)
        data = dict(filter=dict(shopping_key=shopping_id))
        return super(PaymentController, self).get_by_data(data, db_session)

    def edit_by_model(self, model, data, db_session, username, schema_checked=False,
                      permission_checked=False):
        logger.info(LogMsg.START, username)
        return super(PaymentController, self).edit_by_model(model, data, db_session, username,
                                                     schema_checked, permission_checked)


payment_controller = PaymentController()
