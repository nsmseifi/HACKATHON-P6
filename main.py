
from bottle import Bottle, run

from app_token.urls import call_router as token_routes
from sign_up.urls import call_router as sign_routes
from user.urls import call_router as user_routes
from receipt.urls import call_router as receipt_routes
from accounts.urls import call_router as account_routes

app = Bottle()

app.catchall = False

token_routes(app)
sign_routes(app)
user_routes(app)
account_routes(app)
receipt_routes(app)



if __name__ == '__main__':
    print('hello world')

    run(host='0.0.0.0', port=7000, debug=True, app=app)





