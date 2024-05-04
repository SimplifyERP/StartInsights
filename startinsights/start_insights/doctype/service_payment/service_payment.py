# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServicePayment(Document):
    pass
    

    
    def after_submit(self):
        new_sales_invoice = frappe.new_doc("Sales Invoice")
        new_sales_invoice.customer = self.get_customer()
        new_sales_invoice.due_date = self.service_booked_date
        new_sales_invoice.append("items",{
            "item_code":self.service_id,
            "qty":1,
            "uom":"Nos",
            "rate":self.amount,
            "amount":self.amount,
        })
        new_sales_invoice.save(ignore_permissions=True)
        frappe.db.commit()
    
    def get_customer(self):
        customer = frappe.db.get_value("Customer",{"custom_user_name":self.login_user},["name"])
        return customer
    