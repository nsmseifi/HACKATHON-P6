from sign_up.fast_signup import signup, signup_store
from user.controllers.user import user_controller
from .controller import html_serve
from bottle import redirect, response


def userSingUp(data, db_session, *args, **kw):
    try:
        signup(data, db_session, *args, **kw)
        return html_serve("succ-signup.html")
    except Exception as e:
        print(e)
        return html_serve("error-signup.html")


def storeSingUp(data, db_session, *args, **kw):
    try:
        signup_store(data, db_session, *args, **kw)
        return html_serve("succ-signup.html")
    except Exception as e:
        print(e)
        return html_serve("error-signup-store.html")

def login(data, db_session, *args, **kw):
    try:
        rtn = user_controller.get_profile(data.get('username'), db_session, *args, **kw)
        if rtn.get("store"):
            response.set_cookie("userid",rtn.get("id"))
            response.set_header("location","/statics/store-home")
            response.status=302
            return response
            page_rtn= html_serve("store-home.tpl.html")
        else:
            page_rtn=html_serve("profile.html")
        page_rtn.set_cookie("userid",rtn.get("id"))
        return page_rtn
    except Exception as e:
        print(e)
        return html_serve("login.html")

