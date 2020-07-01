from .controller import receipt_controller
from helper import check_auth, inject_db, jsonify, pass_data, timeit,check_unrequirde_auth


def call_router(app):
    wrappers = [inject_db,jsonify,check_unrequirde_auth]
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/receipts/<id>', 'GET', receipt_controller.get, apply=wrappers)
    app.route('/receipts/pay/<id>', 'GET', receipt_controller.pay, apply=wrappers)
    app.route('/receipts/user', 'GET', receipt_controller.user_receipts, apply=wrappers)
    app.route('/receipts/store/<store_id>', 'GET', receipt_controller.store_receipts, apply=wrappers)
    app.route('/receipts/<id>', 'DELETE', receipt_controller.delete, apply=[check_auth, inject_db,timeit])
    app.route('/receipts', 'POST', receipt_controller.add, apply=[inject_db,pass_data])
    app.route('/receipts/_search', 'POST', receipt_controller.get_all_by_data, apply=data_plus_wrappers)
    app.route('/receipts/<id>', 'PUT', receipt_controller.edit, apply=data_plus_wrappers)
