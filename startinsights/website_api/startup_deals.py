import frappe
from frappe.utils import get_url

@frappe.whitelist()
def get_startup_deal(user_id):
    redeem_status = ""
    try:
        startup_deals = frappe.db.get_all("Startup Deals", filters={}, fields=['*'])
        formatted_startup_deals = []

        for startup in startup_deals:
            image_url = get_url() + startup.attach_image if startup.attach_image else ""
            get_reedem_status = frappe.db.exists("Startup Deal Redeem User",{'start_up_deal_id':startup.name,'redeem_user':user_id})
            if get_reedem_status:
                redeem_status = True
            else:
                redeem_status = False    
            startup_dict = {
                "id":startup.name,
                "name":startup.name,
                "service_provider_name": startup.service_provider_name,
                "service_headline": startup.service_headline,
                "attach_image": image_url,
                "short_description": startup.short_description,
                "feature_service": startup.feature_service,
                "popular_service": startup.popular_service,
                "redeem_status":redeem_status,
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

@frappe.whitelist()
def redeem_code(name):
    try:
        codes = frappe.get_all('Startup Deals', filters={'name': name}, fields=['name', 'redeem_code', 'redeem__url', 'redeem_description', 'special_deal'])
        
        formatted_code_list = []
        for code in codes:
            if code.get('special_deal') == "No":
                code_data = {
                    'id': code.name,
                    'name': code.name,
                    'redeem_code': code.redeem_code,
                    'redeem_url': "",
                    'redeem_description': code.redeem_description
                }
            elif code.get('special_deal') == "Yes":
                code_data = {
                    'id': code.name,
                    'name': code.name,
                    'redeem_code':"",
                    'redeem_url': code.redeem__url,
                    'redeem_description': code.redeem_description
                }
            formatted_code_list.append(code_data)

        if formatted_code_list:
            return {"status": True, "redeem_code": formatted_code_list}
        else:
            return {"status": False, "message": "No data found for the specified name."}

    except frappe.DoesNotExistError:
        return {"status": False, "message": "Document does not exist."}
    except Exception as e:
        return {"status": False, "message": f"An error occurred while processing the request: {str(e)}"}

@frappe.whitelist()
def startup_redeem_status_update(start_up_deal_id,user_id):
    try:
        if not frappe.db.exists("Startup Deal Redeem User",{'start_up_deal_id':start_up_deal_id}):
            new_startup_redeem = frappe.new_doc("Startup Deal Redeem User")
            new_startup_redeem.start_up_deal_id = start_up_deal_id
            new_startup_redeem.redeem_status = "Redeemed"
            new_startup_redeem.redeem_user = user_id
            new_startup_redeem.save(ignore_permissions=True)
            new_startup_redeem.submit()
            frappe.db.commit()
            frappe.db.set_value("Startup Deal Redeem User",new_startup_redeem.name,'owner',user_id)
        return {"status":True,"message":"Redeem Copied"}    
    except Exception as e:
        return {"status":False,"message":e}

