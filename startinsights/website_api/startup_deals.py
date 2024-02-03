
import frappe
from frappe.utils import get_url

@frappe.whitelist()
def get_startup_deal():
    try:
        startup_deals = frappe.db.get_all("Startup Deals", filters={}, fields=['*'])
        formatted_startup_deals = []

        for startup in startup_deals:
            image_url = get_url() + startup.attach_image if startup.attach_image else ""
            
            startup_dict = {
                "service_provider_name": startup.service_provider_name,
                "service_headline": startup.service_headline,
                "attach_image": image_url,
                "short_description": startup.short_description,
                "feature_service": startup.feature_service,
                "popular_service": startup.popular_service,
                "startup": []
            }

            startup_list = frappe.get_all('Service Providing List', filters={'parent': startup.name}, fields=['type_of_service'])

            for start in startup_list:
                startup_dict['startup'].append({
                    "type_of_service": start.type_of_service,
                })

            formatted_startup_deals.append(startup_dict)

        return {"status": True, "data": formatted_startup_deals}

    except Exception as e:
        return {"status": False, "message": str(e)}


import frappe

@frappe.whitelist()
def redeem_code(name):
    try:
        codes = frappe.get_all('Startup Deals', filters={'name': name}, fields=['name', 'redeem_code'])
        
        formatted_code_list = []
        for code in codes:
            code_data = {
                'id': code.name,
                'name': code.name,
                'redeem_code': code.redeem_code
            }
            
            formatted_code_list.append(code_data)

        if formatted_code_list:
            return {"status": True, "redeem_code": formatted_code_list}
        else:
            return {"status": False, "message": "No data found for the specified name."}

    except frappe.DoesNotExistError:
        return {"status": False, "message": "Document does not exist."}
    except Exception as e:
        frappe.log_error(f"Error in redeem_code: {str(e)}")
        return {"status": False, "message": "An error occurred while processing the request."}
