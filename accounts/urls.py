from helper import check_auth, inject_db, jsonify, pass_data
from .controller import account_controller


def call_router(app):
    wrappers = [check_auth,inject_db,jsonify]
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/accounts/<id>', 'GET', account_controller.get_by_id, apply=wrappers)
    app.route('/accounts/person/<person_id>', 'GET',
              account_controller.get_person_accounts,
              apply=wrappers)
    app.route('/accounts/<id>', 'PUT', account_controller.edit, apply=data_plus_wrappers)
    app.route('/accounts/user/_search', 'POST', account_controller.get_user_accounts,
              apply=data_plus_wrappers)
    app.route('/accounts/_search', 'POST', account_controller.get_all,
              apply=data_plus_wrappers)
    app.route('/accounts', 'POST', account_controller.add, apply=data_plus_wrappers)
    app.route('/accounts/<id>', 'DELETE', account_controller.delete,
              apply=[check_auth, inject_db])
    app.route('/accounts', 'DELETE', account_controller.delete_all,
              apply=[check_auth, inject_db])
    app.route('/accounts', 'PUT', account_controller.edit_by_person,
              apply=data_plus_wrappers)
