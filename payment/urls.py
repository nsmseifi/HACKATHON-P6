from helper import check_auth, inject_db, jsonify, pass_data, timeit
from payment.controllers.payment import payment_controller


def call_router(app):
    wrappers = [check_auth, inject_db, jsonify, timeit]
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/payments/_search', 'POST', payment_controller.get_all,
              apply=data_plus_wrappers)
