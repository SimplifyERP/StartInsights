import frappe
from datetime import datetime
from frappe.utils import now, getdate, today, format_date



@frappe.whitelist()
def create_investor(user_id,investor_name,investor_email,firm_name,status,amount,date,notes):
    try:
        contact_date_format = datetime.strptime(date, "%d-%m-%Y").date()
        new_investor = frappe.new_doc("User Created Investors")
        new_investor.investor_name = investor_name
        new_investor.investor_email = investor_email
        new_investor.firm_name = firm_name
        new_investor.status = status
        new_investor.amount = amount
        new_investor.first_contact = contact_date_format
        new_investor.notes = notes
        new_investor.creation_user = user_id
        new_investor.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.db.set_value("User Created Investors",new_investor.name,'owner',user_id)
        return {"status":True,"message":"New Investor Created"}
    except Exception as e:
        return {"status":False,"message":e}


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
                "first_contact":format_date(investors.first_contact),
                "notes":investors.notes
            }
            investors_list.append(user_investors)
        return {"status":True,"user_investors":investors_list}    
    except Exception as e:
        return {"status":False,"message":e}
    
@frappe.whitelist()
def update_investor_status(investor_id,status):
    try:
        frappe.db.set_value("User Created Investors",investor_id,"status",status)
        get_investor_status = frappe.get_doc("User Created Investors",investor_id)
        return {"status":True,"investor_status":get_investor_status.status}
    except Exception as e:
        return {"status":False,"message":e}
