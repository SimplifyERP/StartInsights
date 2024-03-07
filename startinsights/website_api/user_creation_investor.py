import frappe
from datetime import datetime
from frappe.utils import now, getdate, today, format_date


#user created investor while creating the status will be sortlist for default
@frappe.whitelist()
def create_investor(user_id,investor_name,investor_email,firm_name,investor_status,amount,contact_no,notes):
    status = ""
    message = ""
    try:
        if not frappe.db.exists('User Created Investors',{'creation_user':user_id,'investor_name':investor_name,'investor_status':investor_status}):
            new_investor = frappe.new_doc("User Created Investors")
            new_investor.investor_name = investor_name
            new_investor.investor_email = investor_email
            new_investor.firm_name = firm_name
            new_investor.investor_status = investor_status
            new_investor.amount = amount
            new_investor.contact_no = contact_no
            new_investor.notes = notes
            new_investor.creation_user = user_id
            new_investor.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("User Created Investors",new_investor.name,'owner',user_id)

            status = True
            message = "New Investor Created"
        else:
            status = True
            message = "Investor Already Created Either Update the status or Add New Investor"      
        return {"status":status,"message":message}
    except Exception as e:
        return {"status":False,"message":e}

#list view the user created investors
@frappe.whitelist()
def get_user_created_investors_list(user_id):
    try:
        created_investors = frappe.db.get_all("User Created Investors",{'creation_user':user_id},['*'])
        investors_list = []
        for investors in created_investors:
            user_investors = {
                "id":investors.name,
                "name":investors.name,
                "investor_name":investors.investor_name,
                "investor_email":investors.investor_email,
                "firm_name":investors.firm_name,
                "status":investors.status,
                "amount":investors.amount,
                "contact_no":investors.contact_no,
                "notes":investors.notes
            }
            investors_list.append(user_investors)
        return {"status":True,"user_investors":investors_list}    
    except Exception as e:
        return {"status":False,"message":e}
    
