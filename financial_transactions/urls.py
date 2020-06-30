from helper import check_auth, inject_db, jsonify, pass_data, timeit
from .controller import transaction_controller


def call_router(app):
    wrappers = [check_auth, inject_db, jsonify, timeit]
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/transactions/<id>', 'GET', transaction_controller.get, apply=wrappers)
    app.route('/transactions/_search', 'POST', transaction_controller.get_all,
              apply=data_plus_wrappers)
    app.route('/transactions/<id>', 'DELETE', transaction_controller.delete,
              apply=[check_auth, inject_db, timeit])
    app.route('/transactions', 'POST', transaction_controller.add,
              apply=data_plus_wrappers)
