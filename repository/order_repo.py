from helper import Http_error, model_basic_dict
from messages import Message
from order.models import Order
from user.controllers.person import person_controller


def get(id, db_session, username=None):
    return db_session.query(Order).filter(Order.id == id).first()


def get_order_dict(id, db_session, username=None):
    order = db_session.query(Order).filter(Order.id == id).first()
    if order is None:
        return None
    return order.to_dict()


def order_count(db_session):
    return db_session.query(Order).count()


def invoice_count(db_session):
    return db_session.query(Order).filter(Order.status == 'Invoiced').count()


# def order_to_dict(order, db_session, username=None):
#     if not isinstance(order, Order):
#         raise Http_error(404, Message.INVALID_ENTITY)
#
#     result = model_basic_dict(order)
#
#     model_props = {
#         'person_id': order.person_id,
#         'price_detail': order.price_detail,
#         'description': order.description,
#         'total_price': order.total_price,
#         'status': order.status.name,
#         'person': order.person.to_dict()
#     }
#     result.update(model_props)
#     return result
