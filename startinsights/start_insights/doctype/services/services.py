# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from frappe import _



class Services(Document):
    pass

@frappe.whitelist()
def set_assign_users(user_list_str,id,service_name):
    try:
        user_list = json.loads(user_list_str)
        users = []
        for item in user_list['assign_user']:
            users.append(item['user'])
            if not frappe.db.exists("Pitch Craft Assign",{'services_id':id}):
                new_pitch_assign = frappe.new_doc("Pitch Craft Assign")
                new_pitch_assign.services_id = id
                new_pitch_assign.assign_user = item['user']
                new_pitch_assign.services_service_name = service_name
                new_pitch_assign.save(ignore_permissions=True)
                new_pitch_assign.submit()
                frappe.db.commit()
            else:
                frappe.throw(_("Pitch Craft Assign Already there for this id %s"%(id)))
    except Exception as e:
        frappe.log_error(f"Error in set_assign_users: {str(e)}")
        return None
