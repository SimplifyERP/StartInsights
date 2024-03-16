import frappe
from frappe.utils import get_url
from startinsights.custom import get_domain_name

@frappe.whitelist()
def get_deal_list(user_id):
    redeem_status = ""
    try:
        deal_list = frappe.db.get_all("Startup Deals", filters={}, fields=['*'])
        deal_list_append = []
        for deal in deal_list:
            if deal.attach_image:
                image_url = get_domain_name() + deal.attach_image
            else:
                image_url = ""    
            get_reedem_status = frappe.db.exists("Startup Deal Redeem User",{'start_up_deal_id':deal.name,'redeem_user':user_id})
            if get_reedem_status:
                redeem_status = True
            else:
                redeem_status = False    
            get_deal = {
                "id":deal.name,
                "name":deal.name,
                "service_provider_name": deal.service_provider_name,
                "attach_image": image_url,
                "service_headline": deal.service_headline,
                "short_description": deal.short_description,
                "feature_service": deal.feature_service,
                "popular_service": deal.popular_service,
                "redeem_status":redeem_status,
                "startup": []
            }
            startup_list = frappe.get_all('Service Providing List', filters={'parent': deal.name}, fields=['type_of_service'])
            for start in startup_list:
                get_deal['startup'].append({
                    "type_of_service": start.type_of_service,
                })
            deal_list_append.append(get_deal)
        return {"status": True, "deal_list": deal_list_append}
    except Exception as e:
        return {"status": False, "message": str(e)}

@frappe.whitelist()
def redeem_code(deal_id):
    try:
        codes = frappe.get_all('Startup Deals', filters={'name': deal_id}, fields=['name', 'redeem_code', 'redeem__url', 'redeem_description', 'special_deal'])
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

#user get the redeem code will new create a new doc to track which user will get the redeem code 
@frappe.whitelist()
def startup_redeem_status_update(start_up_deal_id,user_id):
    status = ""
    message = ""
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
            status = True
            message = "Redeem Code Copied"
        else:
            status = False
            message = "Already Redeem Code Copied"
        return {"status":status,"message":message}    
    except Exception as e:
        return {"status":False,"message":e}

