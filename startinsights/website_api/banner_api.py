import frappe
from startinsights.custom import get_domain_name


@frappe.whitelist()
def get_banner(type_of_user):
    try:
        get_banner_data = frappe.db.get_all("Dashboard Banner",{"disabled":1},['*'])
        for banner in get_banner_data:
            if banner.customer_group == type_of_user:
                pass
        return {"status":True}
    except Exception as e:
        return {"status":False,"message":e}