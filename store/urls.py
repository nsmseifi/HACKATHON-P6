from store.controller import store_controller
from helper import check_auth, inject_db, jsonify, pass_data, timeit


def call_router(app):
    wrappers = [inject_db,check_auth,jsonify]
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/stores/<id>', 'GET', store_controller.get, apply=wrappers)
    app.route('/stores/<id>', 'DELETE', store_controller.delete, apply=[check_auth, inject_db,timeit])
    app.route('/stores', 'POST', store_controller.add, apply=data_plus_wrappers)
    app.route('/stores/_search', 'POST', store_controller.search_store, apply=data_plus_wrappers)
    app.route('/stores/<id>', 'PUT', store_controller.edit, apply=data_plus_wrappers)
    app.route('/stores/profile', 'GET', store_controller.get_profile, apply=wrappers)
