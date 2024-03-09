# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ProfileApplication(Document):
	def after_insert(self):
		# Check if the user_name already exists in Customer doctype
		if not frappe.db.exists("Customer", {"user_name": self.user_id}):
			get_lead = frappe.db.get_value("Lead",{'email_id':self.user_id},['name'])
			if get_lead: 
				new_customer = frappe.new_doc("Customer")
				new_customer.customer_name = self.full_name
				new_customer.custom_user_name = self.user_id
				new_customer.lead_name = get_lead
				new_customer.customer_type = "Individual"
				new_customer.customer_group = self.customer_group
				new_customer.custom_profile_id = self.name
				new_customer.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Lead",get_lead,"custom_customer_group",self.customer_group)
				
				