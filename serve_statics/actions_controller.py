from sign_up.fast_signup import signup, signup_store
from user.controllers.user import user_controller
from .controller import html_serve
from bottle import redirect, response, SimpleTemplate, HTTPResponse
from receipt.controller import receipt_controller
from helper import dir_path
import os
def get_tpl_addr():
    return os.path.join(dir_path,"statics")


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

def pay_receipt(rcp_id,data,db_session, username=None,*args,**kwargs):
    if 'login' in data:
        return redirect("/statics/login.html")
    elif 'paypal' in data:
        return SimpleTemplate(source="Paypal Does Not Implemented Yet.").render()
    elif 'pay_by_account' in data:
        try:
            receipt_controller.pay(rcp_id,db_session,username)
            return SimpleTemplate(name="succ_pay.tpl",lookup=[get_tpl_addr(), os.path.join(get_tpl_addr(),"receipt")]).render()
        except HTTPResponse as e:
            return SimpleTemplate(name="general_error.tpl",lookup=[get_tpl_addr()]).render(error=e.body)
        except Exception as e:
            return SimpleTemplate(name="general_error.tpl",lookup=[get_tpl_addr()]).render(error=str(e))
