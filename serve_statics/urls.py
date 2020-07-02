from .controller import js_serve, fonts_serve, css_serve, images_serve, html_serve
from .actions_controller import userSingUp, storeSingUp, login
from .dynpages_controller import home_store, store_receipts, store_add_new_receipt_page, store_add_new_receipt,show_receipt_to_pay
from helper import check_auth, inject_db, jsonify, pass_data, timeit, \
    check_unrequirde_auth


def call_router(app):
    wrappers = [check_unrequirde_auth]
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/statics/js/<filename>', 'GET', js_serve, apply=wrappers)
    app.route('/statics/css/<filename>', 'GET', css_serve, apply=wrappers)
    app.route('/statics/fonts/<filename>', 'GET', fonts_serve, apply=wrappers)
    app.route('/statics/images/<filename>', 'GET', images_serve, apply=wrappers)
    app.route('/statics/<filename>', 'GET', html_serve, apply=wrappers)

    app.route('/statics/userSignUp','POST',userSingUp,apply=[pass_data,inject_db])
    app.route('/statics/storeSignUp','POST',storeSingUp,apply=[pass_data,inject_db])
    app.route('/statics/login','POST',login,apply=[pass_data,inject_db])
    app.route('/statics/store-home','GET',home_store,apply=[pass_data,inject_db,check_auth])
    app.route('/statics/store-reciepts','GET',store_receipts,apply=[pass_data,inject_db,check_auth])
    app.route('/statics/add-new-receipt','GET',store_add_new_receipt_page,apply=[pass_data,inject_db,check_auth])
    app.route('/statics/add-new-receipt','POST',store_add_new_receipt,apply=[pass_data,inject_db,check_auth])
    app.route('/statics/show-receipt/<rcp_id>','GET',show_receipt_to_pay,apply=[pass_data,inject_db,check_unrequirde_auth])