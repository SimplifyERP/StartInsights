# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class UserCreatedInvestors(Document):
	def after_insert(self):
		#checking that already funding crm is created the same user and the same type of investor
		if not frappe.db.exists("Funding CRM",{"user_id":self.creation_user,"type_of_investor":"User Created Investors","user_created_investor":self.name}):
			new_crm = frappe.new_doc("Funding CRM")
			new_crm.user_id = self.creation_user
			new_crm.type_of_investor = "User Created Investors"
			new_crm.funding_crm_status = self.investor_status
			new_crm.user_created_investor = self.name
			new_crm.save(ignore_permissions=True)
			frappe.db.commit()

