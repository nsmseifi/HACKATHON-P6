import hashlib
import json

from bottle import response

from accounts.controller import account_controller
from check_permission import validate_permissions_and_access
from controller_model import BasicController
from enums import OrderStatus, Access_level
from infrastructure.schema_validator import schema_validate
from order.controllers.order_items import order_item_controller
from prices.controller import price_controller
from repository.user_repo import check_user
from order.models import Order
from book_library.controller import library_cotroller
from repository.item_repo import get_orders_items_internal
from helper import Http_error, Http_response, value
from log import LogMsg, logger
from messages import Message
from financial_transactions.controller import transaction_controller as transaction
from ..constants import ORDER_ADD_SCHEMA_PATH, ORDER_EDIT_SCHEMA_PATH, \
    CHECKOUT_EDIT_SCHEMA_PATH
from ..repository import OrderRepository

administrator_users = value('administrator_users', ['admin'])

order_schemas = dict(add=ORDER_ADD_SCHEMA_PATH, edit=ORDER_EDIT_SCHEMA_PATH)
order_permissions = dict(add='ORDER_ADD', edit='ORDER_EDIT', get='ORDER_GET',
                         delete='ORDER_DELETE')


class OrderController(BasicController):

    def __init__(self):
        super(OrderController, self).__init__(Order, OrderRepository, order_schemas,
                                              order_permissions)

    def exists(self, id, db_session):
        query_data = dict(filter=dict(id=id))
        res = super(OrderController, self).get_by_data(query_data, db_session)
        if res is None:
            return False
        return res

    def add(self, data, db_session, username, schema_checked=False,
            permission_checked=False):
        logger.info(LogMsg.START, username)
        user = check_user(username, db_session)
        if 'person_id' not in data:
            data['person_id'] = user.person_id
            permission_checked = True
        model_instance = super(OrderController, self).add(data, db_session, username,
                                                          schema_checked,
                                                          permission_checked)
        if data.get('items', None) is not None:
            item_data = {}
            item_data['items'] = data.get('items')
            item_data['person_id'] = data.get('person_id')
            logger.debug(LogMsg.ORDER_ADD_ITEMS, data.get('items'))
            model_instance.total_price = order_item_controller.add_orders_items(
                model_instance.id,
                item_data, db_session,
                username)

        order_dict = self.to_dict(model_instance, db_session)
        logger.debug(LogMsg.ORDER_ADD, order_dict)
        logger.info(LogMsg.END)
        return order_dict

    def get(self, id, db_session, username=None):
        logger.info(LogMsg.START, username)
        result = super(OrderController, self).get(id, db_session, username)
        return self.to_dict(result, db_session)

    def get_all(self, data, db_session, username=None, permission_checked=False):
        logger.info(LogMsg.START, username)
        result = super(OrderController, self).get_all(data, db_session, username,
                                                      permission_checked)
        res = [self.to_dict(item, db_session) for item in result]
        logger.info(LogMsg.END)
        return res

    def get_user_orders(self, data, db_session, username=None):
        logger.info(LogMsg.START, username)
        user = check_user(username, db_session)
        if data.get('filter') is None:
            data.update({'filter': {'person_id': user.person_id}})
        else:
            data['filter'].update({'person_id': user.person_id})

        return self.get_all(data, db_session, username, True)

    def get_person_orders(self, data, db_session, username=None):
        logger.info(LogMsg.START, username)
        result = super(OrderController, self).get_all(data, db_session, username, False,
                                                      Access_level.Premium)
        res = [self.to_dict(item, db_session) for item in result]
        logger.debug(LogMsg.ORDER_USER_ORDERS, res)
        logger.info(LogMsg.END)
        return res

    def delete(self, id, db_session, username=None):
        logger.info(LogMsg.START, username)

        order = self.exists(id, db_session)
        if not order:
            logger.error(LogMsg.NOT_FOUND, {'order_id': id})
            raise Http_error(404, Message.NOT_FOUND)

        if order.status == OrderStatus.Invoiced:
            logger.error(LogMsg.ORDER_NOT_EDITABLE,
                         order.to_dict())
            raise Http_error(403, Message.ORDER_INVOICED)
        user = check_user(username, db_session)
        permission_checked = False

        if order.person_id == user.person_id or order.creator == username:
            permission_checked = True
        try:
            logger.debug(LogMsg.ORDER_ITEMS_DELETE, {'order_id': id})
            order_item_controller.delete_orders_items_internal(order.id, db_session)
            logger.debug(LogMsg.ORDER_DELETE, {'order_id': id})
            super(OrderController, self).delete_by_model(order, db_session, username,
                                                         permission_checked=permission_checked,
                                                         access_level=Access_level.Premium)
        except:
            logger.exception(LogMsg.DELETE_FAILED, exc_info=True)
            raise Http_error(403, Message.ACCESS_DENIED)
        logger.info(LogMsg.END)
        return Http_response(204, True)

    def edit(self, id, data, db_session, username=None):
        logger.info(LogMsg.START, username)
        model_instance = self.exists(id, db_session)
        logger.debug(LogMsg.ORDER_CHECK, {'order_id': id})
        if model_instance is None:
            logger.error(LogMsg.NOT_FOUND, {'order_id': id})
            raise Http_error(404, Message.NOT_FOUND)

        if model_instance.status == OrderStatus.Invoiced:
            logger.error(LogMsg.ORDER_NOT_EDITABLE, {'order_id': id})
            raise Http_error(403, Message.ORDER_INVOICED)

        user = check_user(username, db_session)
        model_instance = super(OrderController, self).edit_by_model(model_instance, data,
                                                                    db_session, username,
                                                                    False, False,
                                                                    Access_level.Premium)
        if 'items' in data:
            item_data = {}
            item_data['items'] = data.get('items')
            if 'person_id' in data:
                item_data['person_id'] = data.get('person_id')
            else:
                item_data['person_id'] = user.person_id
            logger.debug(LogMsg.ORDER_ITEMS_DELETE, {'order_id': id})
            order_item_controller.delete_orders_items_internal(model_instance.id,
                                                               db_session)
            logger.debug(LogMsg.ORDER_ADD_ITEMS, {'order_id': id})
            model_instance.total_price = order_item_controller.add_orders_items(
                model_instance.id
                , item_data,
                db_session, username)
        order_dict = self.to_dict(model_instance, db_session)
        logger.debug(LogMsg.MODEL_ALTERED, order_dict)

        logger.info(LogMsg.END)
        return order_dict

    def edit_status_internal(self, id, status, db_session, username=None):
        logger.info(LogMsg.START, username)

        model_instance = self.exists(id, db_session)
        logger.debug(LogMsg.ORDER_CHECK, {'order_id': id})
        if model_instance is None:
            logger.error(LogMsg.NOT_FOUND, {'order_id': id})
            raise Http_error(404, Message.NOT_FOUND)
        try:
            data = dict(status=status)
            super(OrderController, self).edit_by_model(model_instance, data, db_session,
                                                       username, True, True)
        except Exception as e:
            logger.exception(LogMsg.EDIT_FAILED, exc_info=True)
            raise Http_error(400, Message.EDIT_FAILED)
        logger.info(LogMsg.END)
        return model_instance

    def checkout(self, order_id, data, db_session, username, schema_checked=False,
                 permission_checked=False):
        logger.info(LogMsg.START, username)

        if not schema_checked:
            schema_validate(data, CHECKOUT_EDIT_SCHEMA_PATH)
            logger.debug(LogMsg.SCHEMA_CHECKED)

        preferred_account = data.get('preferred_account', 'Main')
        logger.debug(LogMsg.ORDER_CHECKOUT_REQUEST, order_id)
        order = self.exists(order_id, db_session)
        if order is None:
            logger.error(LogMsg.NOT_FOUND, {'order_id': order_id})
            raise Http_error(404, Message.NOT_FOUND)
        logger.debug(LogMsg.ORDER_EXISTS, order_id)

        if order.status == OrderStatus.Invoiced:
            logger.debug(LogMsg.ORDER_NOT_EDITABLE, order_id)
            raise Http_error(409, Message.ORDER_INVOICED)

        # CHECK PERMISSION
        if not permission_checked:
            logger.debug(LogMsg.PERMISSION_CHECK, username)
            validate_permissions_and_access(username, db_session,
                                            'ORDER_CHECKOUT', model=order)
            logger.debug(LogMsg.PERMISSION_VERIFIED, username)

        logger.debug(LogMsg.GETTING_ACCOUNT_PERSON, {'person_id': order.person_id})
        account = account_controller.get(order.person_id, preferred_account, db_session)
        if account is None:
            logger.error(LogMsg.USER_HAS_NO_ACCOUNT,
                         {'person_id': order.person_id, 'type': preferred_account})
            raise Http_error(404, Message.USER_HAS_NO_ACCOUNT)

        logger.debug(LogMsg.ORDER_CALC_PRICE, {'order_id', order_id})
        order_price = order_item_controller.recalc_order_price(order_id, db_session)
        logger.debug(LogMsg.ORDER_CHECK_ACCOUNT_VALUE)
        if account.value < order_price:
            logger.error(LogMsg.ORDER_LOW_BALANCE,
                         {'order_price': order_price, 'account_value': account.value})
            raise Http_error(402, Message.INSUFFICIANT_BALANCE)

        account.value -= order_price

        transaction_data = {'account_id': account.id, 'debit': order_price}

        transaction.internal_add(transaction_data, db_session)

        order = self.edit_status_internal(order_id, OrderStatus.Invoiced, db_session)
        logger.debug(LogMsg.ORDER_INVOICED, order_id)

        order_items = get_orders_items_internal(order_id, db_session)
        logger.debug(LogMsg.ORDER_GETTING_ITEMS, {'order_id': order_id})
        book_list = []
        for item in order_items:
            book_list.append(item.book_id)

        library_cotroller.add_books_to_library(order.person_id, book_list, db_session)
        data.update({'order_price': order_price})
        logger.debug(LogMsg.ORDER_ITEMS_ADDED_TO_LIB)
        logger.info(LogMsg.END)
        return self.to_dict(order, db_session)

    def free_books_order(self, data, db_session, username):
        logger.info(LogMsg.START, username)
        schema_validate(data, ORDER_ADD_SCHEMA_PATH)
        items = [item.get('book_id') for item in data.get('items')]
        user = check_user(username, db_session)
        person_id = data.get('person_id') or user.person_id
        if not price_controller.check_books_be_free(items, db_session):
            logger.error(LogMsg.PRICE_IS_NOT_FREE, {'book_list': items})
            raise Http_error(400, Message.BOOK_IS_NOT_FREE)
        order = self.add(data, db_session, username, True, True)
        self.checkout(order.get('id'), {'person_id': person_id}, db_session, username,
                      True, True)
        logger.debug(LogMsg.ORDER_ITEMS_ADDED_TO_LIB)
        logger.info(LogMsg.END)
        return order

    def get_shopping_cart(self, db_session, username):
        logger.info(LogMsg.START, username)
        user = check_user(username, db_session)
        data = {'status': 'Created', 'tags': 'Shopping_cart', 'person_id': user.person_id}
        order = self.search_in_tags(data, db_session)
        if len(order) == 1:
            shopping_card_order = order[0]
        elif len(order) > 1:
            shopping_card_order = order[0]

        elif len(order) == 0:
            try:
                shopping_card_order = self.add({'tags': ['Shopping_cart']}, db_session,
                                               username, True, True)
            except:
                logger.error(LogMsg.SHOPPING_CART_ADDITION_FAILD)
                return self.get_shopping_cart(db_session, username)
        logger.info(LogMsg.END)

        if isinstance(shopping_card_order, dict):
            return shopping_card_order
        return self.to_dict(shopping_card_order, db_session)


    def head_shopping_cart(self, db_session, username):
        logger.info(LogMsg.START)

        result = self.get_shopping_cart( db_session, username)
        result_str = json.dumps(result).encode()
        result_hash = hashlib.md5(result_str).hexdigest()

        response.add_header('content_type', 'application/json')
        response.add_header('etag', result_hash)

        logger.info(LogMsg.END)
        return response


    def get_shopping_cart_internal(self, db_session, username):
        logger.info(LogMsg.START, username)
        user = check_user(username, db_session)
        if user.person_id is None:
            logger.error(LogMsg.PERSON_NOT_EXISTS, {'username': username})
            raise Http_error(404, Message.INVALID_PERSON)
        data = {'status': 'Created', 'tags': 'Shopping_cart', 'person_id': user.person_id}
        order = self.search_in_tags(data, db_session)
        if len(order) == 1:
            shopping_card_order = order[0]
        elif len(order) == 0:
            try:
                shopping_card_order = self.add(
                    {'tags': ['Shopping_cart']}, db_session, username, True, True)
            except:
                logger.exception(LogMsg.SHOPPING_CART_ADDITION_FAILD, exc_info=True)
                return self.get_shopping_cart(db_session, username)
        if isinstance(shopping_card_order, Order):
            shopping_card_order = self.to_dict(shopping_card_order, db_session)
        return shopping_card_order

    def add_to_shopping_cart(self, data, db_session, username):
        logger.info(LogMsg.START, username)

        shopping_card = self.get_shopping_cart_internal(db_session, username)
        if shopping_card is None:
            logger.error(LogMsg.NOT_FOUND, {'user_shopping_cart': username})

        data['person_id'] = shopping_card.get('person_id')
        order_item_controller.add_orders_items(shopping_card.get('id'), data, db_session,
                                               username)
        logger.info(LogMsg.END)
        return shopping_card


    def delete_shopping_cart(self,db_session,username):
        logger.info(LogMsg.START,username)
        user = check_user(username,db_session)
        data = {'status': 'Created', 'tags': 'Shopping_cart', 'person_id': user.person_id}
        order = self.search_in_tags(data, db_session)
        if len(order)==0:
            logger.debug(LogMsg.NO_SHOPPING_CART,{'person_id':user.person_id})
            return Http_response(204,True)
        sh_cart = order[0]
        order_item_controller.delete_orders_items_internal(sh_cart.id,db_session)
        super(OrderController, self).delete_by_model(sh_cart,db_session,username,True)
        logger.info(LogMsg.END)
        return Http_response(204,True)

    def delete_shopping_card_items(self, order_item_id, db_session, username):
        logger.info(LogMsg.START, username)
        item = order_item_controller.exists(order_item_id, db_session)
        if not item:
            logger.error(LogMsg.NOT_FOUND, {'order_item': order_item_id})
            raise Http_error(404, Message.NOT_FOUND)

        sh_cart = self.get_shopping_cart_internal(db_session,username)
        if sh_cart.get('id') != item.order_id:
            logger.error(LogMsg.ORDER_ITEM_IS_NOT_INSHOPPING_CART,order_item_id)
            raise Http_error(404, Message.NOT_IN_SHOPPING_CART)
        order_item_controller.delete_by_model(item,db_session,username,True)
        logger.info(LogMsg.END)
        return Http_response(204, True)


    def to_dict(self, model, db_session):
        result = model.to_dict()
        result['items'] = order_item_controller.get_orders_items(model.id,
                                                                 db_session)
        model.total_price = order_item_controller.recalc_order_price(model.id, db_session)
        result['total_price'] = model.total_price
        return result


order_controller = OrderController()
