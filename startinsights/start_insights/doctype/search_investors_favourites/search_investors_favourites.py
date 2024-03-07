# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SearchInvestorsFavourites(Document):
	def after_insert(self):
		if not frappe.db.exists("Funding CRM",{"user_id":self.user_id,"type_of_investor":"User Created Investors","user_created_investor":self.name}):
			new_crm = frappe.new_doc("Funding CRM")
			new_crm.user_id = self.user_id
			new_crm.type_of_investor = "Search Investors"
			new_crm.funding_crm_status = "SORTLIST"
			new_crm.search_investor_favourite = self.name
			new_crm.save(ignore_permissions=True)
			frappe.db.commit()

			get_search_investors_recommended_count = frappe.db.get_value("Search Investors",{'name':self.investors},["recommended_investors_count"])
			if get_search_investors_recommended_count:
				add_shortlist_count = get_search_investors_recommended_count + 1
				frappe.db.set_value("Search Investors",self.investors,"recommended_investors_count",add_shortlist_count)