from .controller import token
from helper import check_auth, inject_db, jsonify, pass_data, wrappers


def call_router(app):
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/tokens/<id>', 'GET', token.get, apply=wrappers)
    app.route('/tokens/<id>', 'DELETE', token.delete, apply=[check_auth, inject_db])
    app.route('/tokens', 'POST', token.add, apply=data_plus_wrappers)
