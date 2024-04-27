# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FundabilityQuizFlow(Document):
	pass
# @frappe.whitelist()
# def get_fundability_quiz_options(question):
#     data = "<h1>Fundability Quiz Options</h1>"
#     # Assuming you're returning a table, format it properly
#     data += "<table>"
#     data += "<tr><th>Column 1 Header</th><th>Column 2 Header</th></tr>"
#     # Example rows, replace with your actual data retrieval logic
#     data += "<tr><td>Data 1</td><td>Data 2</td></tr>"
#     data += "<tr><td>Data 3</td><td>Data 4</td></tr>"
#     data += "</table>"
#     return [data]  # Returning as a list, each element representing a row
