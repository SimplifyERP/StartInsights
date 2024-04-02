import frappe
from startinsights.custom import get_domain_name


@frappe.whitelist()
def get_banner(type_of_user):
    banner_image_url = ""
    try:
        get_banner_data = frappe.db.get_all("DashBoard Banner",{"customer_group":type_of_user},['*'])
        banner_list = []
        for banner in get_banner_data:
            if banner.banner_image:
                banner_image_url = get_domain_name() + banner.default_banner_image
            else:
                banner_image_url = ""    
            banner_details = {
                "id":banner.name,
                "name":banner.name,
                "title":banner.banner_name or "",
                "description":banner.description or "   ",
                "banner_type":banner.type_of_banner or "",
                "banner_image":banner_image_url,
                "type_of_user":banner.customer_group or "",
                "ad_start_date":banner.ad_start_date_time or "",
                "ad_end__time":banner.ad_end_date_time or ""
            }
            banner_list.append(banner_details)
                
        return {"status":True,"banner":banner_list}
    except Exception as e:
        return {"status":False,"message":e}