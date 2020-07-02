from repository.user_repo import check_user
from .controller import html_serve
from bottle import SimpleTemplate
from helper import dir_path
import os
from bottle import TEMPLATE_PATH
from receipt.controller import receipt_controller
from user.controllers.person import  person_controller
import datetime
from bottle import HTTPResponse

def get_tpl_path():
    return os.path.join(dir_path, "statics")
TEMPLATE_PATH.append(get_tpl_path())

def home_store(data,db_session,username, *args,**kwargs):
    user = check_user(username,db_session)
    page_rtn=SimpleTemplate(name="store-home.tpl.html",lookup=[get_tpl_path()])
    # page_rtn=html_serve("store-home.tpl.html")
    return page_rtn.render(user=user)

def store_receipts(data,username,db_session, *args,**kwargs):
    user=check_user(username,db_session)
    data=dict(filter=dict(payee_id=user.person.id))
    receipts = receipt_controller.get_all_by_data(data,db_session)
    page_rtn = SimpleTemplate(name="receipts_list.tpl",lookup=[get_tpl_path()])
    # receipts=[x.to_dict() for x in receipts if x is not None]
    for r in receipts:
        r.creation_date_1=datetime.datetime.fromtimestamp(r.creation_date)
    return page_rtn.render(receipts=receipts)

def store_add_new_receipt_page(data,username,db_session,*args,**kwargs):
    page_rtn=SimpleTemplate(name="receipt_form.tpl",lookup=[get_tpl_path()])
    return page_rtn.render()
def store_add_new_receipt(data,username,db_session,*args,**kwargs):
    items=[]
    for i in range(100):
        if 'prd_{}'.format(i) not in data:
            break
        else:
            item=dict(name=data.get("prd_{}".format(i)),
                      qty=data.get("qty_{}".format(i)),
                      price=data.get("price_{}".format(i)))
            items.append(item)
    user=check_user(username,db_session)
    rcp_data=dict(payee_id=user.person.id, status="Waiting", title=data.get("title"),
                  total_payment=float(data.get("total_amount",0)),
                  hst=float(data.get("hst",0)),
                  subtotal=float(data.get("subtotal",0)),
                  payer_name=data.get("payer"),
                  body=items)
    try:
        return receipt_controller.add(db_session,rcp_data,username)
    except HTTPResponse as e:
        return SimpleTemplate(name="receipt_form_error.tpl",lookup=[get_tpl_path()]).render(error=e.body)

    except Exception as e:

        return SimpleTemplate(name="receipt_form_error.tpl",lookup=[get_tpl_path()]).render(error=e)



    pass


def show_receipt_to_pay(rcp_id,data,db_session,username=None, *args,**kwargs):
    page_rtn=SimpleTemplate(name="show_receipt.tpl",lookup=[os.path.join(get_tpl_path(),"receipt")])
    user=check_user(username,db_session) if username else username
    try:
        rcp= receipt_controller.get(rcp_id,db_session)
        rcp["creation_date_1"]=datetime.date.fromtimestamp(rcp.get("creation_date",0))
        rcp["store"]= person_controller.get(rcp["payee_id"],db_session)
        if user:
            b = person_controller.get(user.person_id,db_session)
            user.person_1=b
        return page_rtn.render(rcp=rcp,user=user)
    except Exception as e:
        raise HTTPResponse(status=404,body="No RECEIPT FOUND.")
    return page_rtn.render()