# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SearchInvestorsFavourites(Document):
	def after_insert(self):
		if not frappe.db.exists("Funding CRM",{"user_id":self.user_id,"type_of_investor":"Search Investors Favourites","search_investor_favourite":self.name}):
			new_crm = frappe.new_doc("Funding CRM")
			new_crm.user_id = self.user_id
			new_crm.type_of_investor = "Search Investors Favourites"
			new_crm.funding_crm_status = "SORTLIST"
			new_crm.search_investor_favourite = self.name
			new_crm.save(ignore_permissions=True)
			frappe.db.commit()

			