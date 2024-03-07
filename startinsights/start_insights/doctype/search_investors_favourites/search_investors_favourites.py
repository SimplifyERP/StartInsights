# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SearchInvestorsFavourites(Document):
	def validate(self):
		if self.favourites_status == 1:
			if frappe.db.exists("Search Investors",{'name':self.investors}):
				frappe.db.set_value("Search Investors",self.investors,'status','In Shortlist')
		else:
			self.favourites_status == 0	
			if frappe.db.exists("Search Investors",{'name':self.investors}):
				frappe.db.set_value("Search Investors",self.investors,'status','')	
