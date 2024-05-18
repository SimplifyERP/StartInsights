import frappe 




def create_startups_customer_group():
    customer_group_list = ["Startups","Investors"]
    for customer in customer_group_list:
        if not frappe.db.exists('Customer Group', customer):
            customer_group = frappe.get_doc({
                'doctype': 'Customer Group',
                'customer_group_name': customer,
                'parent_customer_group': 'All Customer Groups',
                'is_group': 0
            })
            customer_group.insert()
            frappe.db.commit()

