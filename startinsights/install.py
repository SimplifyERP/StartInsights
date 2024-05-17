import frappe 




def create_startups_customer_group():
    if not frappe.db.exists('Customer Group', 'Startups'):
        customer_group = frappe.get_doc({
            'doctype': 'Customer Group',
            'customer_group_name': 'Startups',
            'parent_customer_group': 'All Customer Groups',
            'is_group': 0
        })
        customer_group.insert()
        frappe.db.commit()

