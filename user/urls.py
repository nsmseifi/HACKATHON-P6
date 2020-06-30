from user.controllers.user import user_controller as user
from user.controllers.person import person_controller as person
from helper import check_auth, inject_db, jsonify, pass_data, timeit


def call_router(app):
    wrappers = [inject_db,check_auth,jsonify]
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)

    app.route('/users/<id>', 'GET', user.get, apply=wrappers)
    app.route('/users/<id>', 'DELETE', user.delete, apply=[check_auth, inject_db,timeit])
    app.route('/users', 'POST', user.add, apply=data_plus_wrappers)
    app.route('/users/_search', 'POST', user.search_user, apply=data_plus_wrappers)
    app.route('/users/<id>', 'PUT', user.edit, apply=data_plus_wrappers)
    app.route('/users/profile', 'GET', user.get_profile, apply=wrappers)


    app.route('/persons', 'POST', person.add, apply=data_plus_wrappers)
    app.route('/persons/<id>', 'GET', person.get, apply=wrappers)
    app.route('/persons/<id>', 'PUT', person.edit, apply=data_plus_wrappers)
    app.route('/persons/<id>', 'DELETE', person.delete, apply=[check_auth, inject_db,timeit])
    app.route('/persons/_search', 'POST', person.search_person, apply=data_plus_wrappers)

