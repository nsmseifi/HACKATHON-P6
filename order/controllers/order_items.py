from book_encription.controllers.prepare_book import is_generated
from book_library.controller import library_cotroller
from books.controllers.book import book_controller
from books.controllers.book_content import content_controller
from check_permission import get_user_permissions, \
    validate_permissions_and_access
from controller_model import BasicController
from enums import Permissions, Access_level
from prices.controller import price_controller
from repository.item_repo import get_orders_items_internal
from order.models import OrderItem
from repository.order_repo import get as get_order
from repository.book_repo import get as get_book
from helper import Http_error, Http_response
from log import LogMsg, logger
from messages import Message
from configs import ONLINE_BOOK_TYPES, ADMINISTRATORS
from repository.order_repo import get_order_dict
from repository.user_repo import check_user
from ..constants import ITEM_ADD_SCHEMA_PATH, ITEM_EDIT_SCHEMA_PATH
from infrastructure.schema_validator import schema_validate
from ..repository import OrderItemRepository

administrator_users = ADMINISTRATORS

order_schemas = dict(add=ITEM_ADD_SCHEMA_PATH, edit=ITEM_EDIT_SCHEMA_PATH)
order_permissions = dict(add='ORDER_ADD', edit='ORDER_ITEM_EDIT_PREMIUM',
                         get='ORDER_ITEM_GET',
                         delete='ORDER_ITEM_DELETE_PREMIUM')


class OrderItemController(BasicController):

    def __init__(self):
        super(OrderItemController, self).__init__(OrderItem, OrderItemRepository,
                                                  order_schemas,
                                                  order_permissions)

    def exists(self, id, db_session):
        query_data = dict(filter=dict(id=id))
        res = super(OrderItemController, self).get_by_data(query_data, db_session)
        if res is None:
            return False
        return res

    def check_existence(self, book_id, order_id, db_session):
        query_data = dict(filter=dict(book_id=book_id, order_id=order_id))
        res = super(OrderItemController, self).get_by_data(query_data, db_session)
        if res is None:
            return False
        return True

    def add_orders_items(self, order_id, data, db_session, username):
        logger.info(LogMsg.START, username)
        total_price = 0.00
        items = data.get('items')
        for item in items:
            item['order_id'] = order_id
            item['person_id'] = data.get('person_id')
            item_instance = self.add(item, db_session, username)
            total_price += item_instance.net_price

            logger.debug(LogMsg.ORDER_ITEM_ADDDED_TO_ORDER,
                         item_instance.to_dict())

        logger.debug(LogMsg.ORDER_TOTAL_PRICE, total_price)
        logger.info(LogMsg.END)

        return total_price

    def add(self, data, db_session, username):
        logger.info(LogMsg.START, username)

        schema_validate(data, ITEM_ADD_SCHEMA_PATH)
        logger.debug(LogMsg.SCHEMA_CHECKED)

        book_id = data.get('book_id')
        person_id = data.get('person_id', None)
        if person_id is None:
            order = get_order(data.get('order_id'), db_session)
            if order is None:
                logger.error(LogMsg.NOT_FOUND, {'order_id': data.get('order_id')})
                raise Http_error(404, Message.NOT_FOUND)
            person_id = order.person_id
        if library_cotroller.is_book_in_library(person_id, book_id, db_session):
            logger.error(LogMsg.ALREADY_IS_IN_LIBRARY, {'book_id': book_id})
            raise Http_error(409, Message.ALREADY_EXISTS)

        book = get_book(book_id, db_session)
        if book is None:
            logger.error(LogMsg.NOT_FOUND, {'book_id': book_id})
            raise Http_error(404, Message.NOT_FOUND)

        if book.type.name in ONLINE_BOOK_TYPES:
            if self.check_existence(book_id, data.get('order_id'), db_session) or data.get(
                    'count') > 1:
                logger.error(LogMsg.BOOK_ONLINE_TYPE_COUNT_LIMITATION)
                raise Http_error(400, Message.ONLINE_BOOK_COUNT_LIMITATION)

            content_id = content_controller.book_has_content(book_id, 'Original',
                                                             db_session)
            if not content_id:
                logger.error(LogMsg.CONTENT_NOT_FOUND, {'book_id': book_id})
                raise Http_error(404, Message.BOOK_HAS_NO_CONTENT)
            # TODO generate book commented
            # if not is_generated(content_id):
            #     logger.error(LogMsg.CONTENT_NOT_GENERATED, {'content_id': content_id})
            #     raise Http_error(404, Message.BOOK_NOT_GENERATED)

        model_instance = super(OrderItemController, self).add(data, db_session, username,
                                                              True, True)
        model_instance.discount = data.get('discount', 0.0)
        model_instance.unit_price = price_controller.get_book_price_internal(
            model_instance.book_id,
            db_session)
        logger.debug(LogMsg.ORDER_ITEM_UNIT_PRICE, model_instance.unit_price)

        model_instance.net_price = price_controller.calc_net_price(
            model_instance.unit_price,
            model_instance.count,
            model_instance.discount)
        logger.debug(LogMsg.ORDER_ITEM_NET_PRICE, model_instance.net_price)

        logger.info(LogMsg.END)

        return model_instance

    def get(self, id, db_session, username=None):
        logger.info(LogMsg.START)
        item = super(OrderItemController, self).get(id, db_session, username, False,
                                                    Access_level.Premium)
        order = get_order(item.order_id, db_session)
        if order is None:
            logger.error(LogMsg.NOT_FOUND, {'order_id': item.order_id})
            raise Http_error(404, Message.NOT_FOUND)

        return self.to_dict(item, db_session)

    def get_all(self, data, db_session, username=None):
        logger.info(LogMsg.START)
        if data.get('sort') is None:
            data['sort'] = ['creation_date-']

        result = super(OrderItemController, self).get_all(data, db_session,
                                                          access_level=Access_level.Premium)
        res = [self.to_dict(item, db_session) for item in result]
        logger.debug(LogMsg.GET_SUCCESS, res)
        logger.info(LogMsg.END)
        return res

    def get_orders_items(self, order_id, db_session, username=None):
        logger.info(LogMsg.START)

        order = get_order(order_id, db_session)
        if order is None:
            logger.error(LogMsg.NOT_FOUND, {'order_id': order_id})
            raise Http_error(404, Message.NOT_FOUND)

        data = dict(filter=dict(order_id=order_id))
        result = self.get_all(data, db_session, username)

        if username is not None:
            user = check_user(username, db_session)
            per_data = {}
            if order.person_id == user.person_id or (
                    result is not None and result[0].get('creator') == username):
                per_data.update({Permissions.IS_OWNER.value: True})
            logger.debug(LogMsg.PERMISSION_CHECK, username)
            validate_permissions_and_access(username, db_session,
                                            'ORDER_ITEM_GET', per_data, model=order,
                                            access_level=Access_level.Premium)
            logger.debug(LogMsg.PERMISSION_VERIFIED, username)

        logger.debug(LogMsg.ORDERS_ITEMS, result)
        logger.info(LogMsg.END)

        return result

    def delete(self, id, db_session, username=None):
        logger.info(LogMsg.START)

        order_item = self.exists(id, db_session)
        if not order_item:
            logger.error(LogMsg.NOT_FOUND, {'order_item_id': id})
            raise Http_error(404, Message.NOT_FOUND)

        order = get_order(order_item.order_id, db_session)

        try:
            super(OrderItemController, self).delete_by_model(order_item, db_session,
                                                             username, True)
            logger.debug(LogMsg.ORDER_ITEM_DELETED, id)
            new_order = self.calc_total_price_order(order.id, db_session)
            logger.debug(LogMsg.ORDER_CALC_PRICE,
                         new_order.to_dict())
        except:
            logger.exception(LogMsg.DELETE_FAILED, exc_info=True)
            raise Http_error(400, Message.DELETE_FAILED)
        logger.info(LogMsg.END)

        return Http_response(204, True)

    def delete_orders_items_internal(self, order_id, db_session):
        logger.info(LogMsg.START)
        data = {'filter': {'order_id': order_id}}
        try:
            super(OrderItemController, self).delete_all_by_data(data, db_session)
        except:
            logger.exception(LogMsg.DELETE_FAILED, exc_info=True)
            raise Http_error(404, Message.NOT_FOUND)
        logger.info(LogMsg.END)

        return Http_response(204, True)

    def edit(self, id, data, db_session, username=None):
        logger.info(LogMsg.START)

        model_instance = self.exists(id, db_session)
        logger.debug(LogMsg.MODEL_GETTING, {'order_item_id': id})

        if not model_instance:
            logger.error(LogMsg.NOT_FOUND, {'order_item_id': id})
            raise Http_error(404, Message.NOT_FOUND)

        order = get_order(model_instance.order_id, db_session)
        if order is None:
            logger.error(LogMsg.NOT_FOUND, {'order_id': model_instance.order_id})
            raise Http_error(404, Message.NOT_FOUND)

        if username is not None:
            logger.debug(LogMsg.PERMISSION_CHECK, username)
            validate_permissions_and_access(username, db_session,
                                            'ORDER_ITEM_DELETE', model=model_instance)
            logger.debug(LogMsg.PERMISSION_VERIFIED, username)

            permissions, presses = get_user_permissions(username, db_session)

        if Permissions.ORDER_ITEM_EDIT_PREMIUM not in permissions:
            if 'unit_price' in data:
                del data['unit_price']
            if 'net_price' in data:
                del data['net_price']
            if 'order_id' in data:
                del data['order_id']
            if 'book_id' in data:
                del data['book_id']

        try:
            model_instance = super(OrderItemController, self).edit_by_model(
                model_instance, data, db_session, username, False, True)
            model_instance.unit_price = price_controller.get_book_price_internal(
                model_instance.book_id,
                db_session)
            logger.debug(LogMsg.ORDER_ITEM_UNIT_PRICE, model_instance.unit_price)

            model_instance.net_price = price_controller.calc_net_price(
                model_instance.unit_price,
                model_instance.count,
                model_instance.discount)
            logger.debug(LogMsg.ORDER_ITEM_NET_PRICE, model_instance.net_price)

        except:
            logger.exception(LogMsg.EDIT_FAILED, exc_info=True)
            raise Http_error(404, Message.DELETE_FAILED)

        order = self.calc_total_price_order(model_instance.order_id, db_session)
        logger.debug(LogMsg.ORDER_CALC_PRICE, order.to_dict())

        logger.info(LogMsg.END)

        return self.to_dict(model_instance, db_session)



    def calc_total_price_order(self, order_id, db_session):
        logger.info(LogMsg.START)

        items = get_orders_items_internal(order_id, db_session)
        order_price = 0.0
        for item in items:
            order_price += item.net_price
        order = get_order(order_id, db_session)
        order.total_price = order_price
        logger.info(LogMsg.END)

        return order

    def recalc_order_price(self, order_id, db_session):
        logger.info(LogMsg.START)

        items = get_orders_items_internal(order_id, db_session)
        order_price = 0.0
        for item in items:
            book_price = price_controller.get_book_price_internal(item.book_id,
                                                                  db_session)
            if item.unit_price != book_price:
                item.unit_price = book_price
                item.net_price = price_controller.calc_net_price(book_price, item.count,
                                                                 item.discount)
            order_price += item.net_price
        logger.info(LogMsg.END)

        return order_price

    def to_dict(self, model, db_session):
        result = model.to_dict()
        result['order'] = get_order_dict(model.order_id, db_session, None)
        result['book'] = book_controller.book_to_dict(model.book,db_session)
        return result


order_item_controller = OrderItemController()
