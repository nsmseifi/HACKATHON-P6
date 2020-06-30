
from bottle import Bottle, run
from helper import generate_RID

from app_token.urls import call_router as token_routes

app = Bottle()

app.catchall = False

token_routes(app)


app.add_hook('before_request',generate_RID)

if __name__ == '__main__':
    print('hello world')

    run(host='0.0.0.0', port=7000, debug=True, app=app)





