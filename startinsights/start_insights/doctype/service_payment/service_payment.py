# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServicePayment(Document):
    pass

    
    # def validate(self):
    #     frappe.errprint("hi")
    #     frappe.errprint(self.create_sales_invoice())

    # def create_sales_invoice(self):
    #     new_sales_invoice = frappe.new_doc("Sales Invoice")
    #     new_sales_invoice.customer = self.get_customer()
    #     new_sales_invoice.due_date = self.service_booked_date
    #     new_sales_invoice.save(ignore_permissions=True)
    #     frappe.db.commit()
    
    # def get_customer(self):
    #     customer = frappe.db.get_value("Customer",{"custom_user_name":self.login_user},["name"])
    #     return customer
    