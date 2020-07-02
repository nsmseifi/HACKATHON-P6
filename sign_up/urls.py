from helper import check_auth, inject_db, jsonify, pass_data, timeit
from .fast_signup import signup,signup_store
def call_router(app):
    wrappers = [check_auth, inject_db, jsonify, timeit]
    data_plus_wrappers = (wrappers[:])
    data_plus_wrappers.append(pass_data)
    app.route('/sign-up', 'POST', signup, apply=[pass_data, inject_db, jsonify, timeit])
    app.route('/sign-up/store', 'POST', signup_store, apply=[pass_data, inject_db, jsonify, timeit])
