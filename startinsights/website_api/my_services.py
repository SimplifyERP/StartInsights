import frappe
from frappe import _
from frappe.utils import now, getdate, today, format_date,format_time
from bs4 import BeautifulSoup
from datetime import datetime

#set the chat coverstations
@frappe.whitelist()
def set_chat_conversation(my_service_id,chat_text):
    try:
        get_my_service = frappe.get_doc("My Services",my_service_id) 
        comment = get_my_service.add_comment("Comment", _(chat_text))
        comment.custom_user = 1
        get_my_service.save()
        comment.save()
        frappe.db.commit()
        return {"status":True,"message":"Comment added successfully"}
    except Exception as e:
        return {"status":False,"message":e}
