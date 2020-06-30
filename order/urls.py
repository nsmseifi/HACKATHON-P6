from helper import check_auth, inject_db, jsonify, pass_data, timeit
from .controllers.order import order_controller as order
from .controllers.order_items import order_item_controller as order_items


def call_router(app):
    wrappers = [check_auth, inject_db, jsonify, timeit]
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/orders', 'POST', order.add, apply=data_plus_wrappers)
    app.route('/orders/_search', 'POST', order.get_all, apply=data_plus_wrappers)
    app.route('/orders/<id>', 'DELETE', order.delete,
              apply=[check_auth, inject_db, timeit])
    app.route('/orders/<id>', 'GET', order.get, apply=wrappers)
    app.route('/orders/shopping-cart', 'GET', order.get_shopping_cart, apply=wrappers)
    app.route('/orders/shopping-cart', 'HEAD', order.head_shopping_cart, apply=[check_auth,inject_db,timeit])
    app.route('/orders/shopping-cart', 'DELETE', order.delete_shopping_cart,
              apply=[check_auth, inject_db, timeit])
    app.route('/orders/shopping-cart/item/<order_item_id>', 'DELETE',
              order.delete_shopping_card_items,
              apply=[check_auth, inject_db, timeit])
    app.route('/orders/shopping-cart', 'POST', order.add_to_shopping_cart,
              apply=data_plus_wrappers)

    app.route('/orders/<id>', 'PUT', order.edit, apply=data_plus_wrappers)
    app.route('/orders/user', 'POST', order.get_user_orders, apply=data_plus_wrappers)
    app.route('/orders/person', 'POST', order.get_person_orders, apply=data_plus_wrappers)

    app.route('/orders/checkout/<order_id>', 'POST', order.checkout,
              apply=data_plus_wrappers)
    app.route('/orders/free-books', 'POST', order.free_books_order,
              apply=data_plus_wrappers)

    app.route('/order-items', 'POST', order_items.add, apply=data_plus_wrappers)
    app.route('/order-items/_search', 'POST', order_items.get_all,
              apply=data_plus_wrappers)
    app.route('/order-items/<id>', 'DELETE', order_items.delete,
              apply=[check_auth, inject_db, timeit])
    app.route('/order-items/<id>', 'GET', order_items.get, apply=wrappers)
    app.route('/order-items/<id>', 'PUT', order_items.edit, apply=data_plus_wrappers)
    app.route('/order-items/order/<order_id>', 'GET', order_items.get_orders_items,
              apply=wrappers)
