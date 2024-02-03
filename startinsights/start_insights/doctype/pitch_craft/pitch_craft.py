# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document


class PitchCraft(Document):
    pass

@frappe.whitelist()
def set_assign_users(user_list):
    list_to_json = json.loads(user_list)
    for user in list_to_json:
        return user
