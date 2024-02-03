# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StartInsightUser(Document):
	# while saving the user type name against role list is creating
	def validate(self):
		if not frappe.db.exists("Role",{'name':self.name}):
			new_role = frappe.new_doc("Role")
			new_role.role_name = self.name
			new_role.save(ignore_permissions=True)
			frappe.db.commit()

