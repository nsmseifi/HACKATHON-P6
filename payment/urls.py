from helper import check_auth, inject_db, jsonify, pass_data, timeit
from payment.controllers.kipo_pay import receive_payment, pay_by_kipo, sample_html_form
from payment.controllers.payment import payment_controller
from payment.controllers.checkout_press_payment import press_payment


def call_router(app):
    wrappers = [check_auth, inject_db, jsonify, timeit]
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/payment-receive', 'GET', receive_payment,
              apply=[inject_db, timeit])
    app.route('/payment-send', 'POST', pay_by_kipo,
              apply=[inject_db, pass_data, check_auth, timeit])
    app.route('/payment-send', 'GET', pay_by_kipo,
              apply=[inject_db, pass_data, check_auth, timeit])

    app.route('/payment-sample', 'GET', sample_html_form,
              apply=[inject_db, pass_data, timeit])

    app.route('/payments/_search', 'POST', payment_controller.get_all,
              apply=data_plus_wrappers)

    app.route('/payment-press-checkouts', 'POST', press_payment.add_payment,
              apply=data_plus_wrappers)
    app.route('/payment-press-checkouts/<id>', 'GET', press_payment.get,
              apply=wrappers)
    app.route('/payment-press-checkouts/total-paid/<person_id>', 'GET',
              press_payment.get_all_paid_for_person,
              apply=wrappers)
    app.route('/payment-press-checkouts/_search', 'POST', press_payment.get_all,
              apply=data_plus_wrappers)
    app.route('/payment-press-checkouts/<id>', 'PUT', press_payment.edit,
              apply=data_plus_wrappers)
    app.route('/payment-press-checkouts/<id>', 'DELETE', press_payment.delete,
              apply=[check_auth, inject_db, timeit])
