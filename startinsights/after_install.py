import frappe 

def after_app_install():
    try:
        create_new_customer_group()
    except Exception as e:
        return e        


def create_new_customer_group():
    try:
        customer_group_name = ["Startups","Investors"]
        if not frappe.db.exists("Customer Group",{'name': customer_group_name}):
            new_customer_group = frappe.new_doc("Customer Group")
            new_customer_group.customer_group_name = customer_group_name
            new_customer_group.save(ignore_permissions=True)
            frappe.db.commit()
    except Exception as e:
        return e