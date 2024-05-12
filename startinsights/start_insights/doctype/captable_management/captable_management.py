# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CaptableManagement(Document):
	
	def validate(self):
		if not self.instrument == "CN":
			self.post_money_valuation = (int(self.pre_money_valuation or 0)) + (int(self.amount_raised or 0))
			percentage = ((int(self.pre_money_valuation or 0)) / (int(self.amount_raised or 0))) * 100
			self.dilution_for_the_round = percentage