import frappe
from datetime import datetime
from frappe.utils import now, getdate, today, format_date
import base64
from startinsights.custom import get_domain_name


#user created investor while creating the status will be sortlist for default
@frappe.whitelist()
def create_investor(user_id,logo,logo_type,logo_name,investor_name,investor_status,contacted_person,funding_stage,description,website,investor_email,contact_no,notes):
    status = ""
    message = ""
    try:
        logo_decode = base64.b64decode(logo)
        new_investor = frappe.new_doc("User Created Investors")
        new_investor.investor_name = investor_name
        new_investor.investor_status = investor_status
        new_investor.contact_person = contacted_person
        new_investor.funding_stage = funding_stage
        new_investor.description = description
        new_investor.website = website
        new_investor.investor_email = investor_email
        new_investor.contact_no = contact_no or ""
        new_investor.notes = notes
        new_investor.creation_user = user_id
        new_investor.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("User Created Investors",new_investor.name,'owner',user_id)

        status = True
        message = "New Investor Created"

        if logo:
            if logo_type in ["png","jpg","jpeg"]:
                file_name_inside = logo_name
                new_file_inside = frappe.new_doc('File')
                new_file_inside.file_name = file_name_inside
                new_file_inside.content = logo_decode
                new_file_inside.attached_to_doctype = "User Created Investors"
                new_file_inside.attached_to_name = new_investor.name
                new_file_inside.attached_to_field = "investor_logo"
                new_file_inside.is_private = 0
                new_file_inside.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.db.set_value("User Created Investors",new_investor.name,'investor_logo',new_file_inside.file_url)
            else:
                message = "You Attached Logo Type is not in Master"
        return {"status":status,"message":message}
    except Exception as e:
        return {"status":False,"message":e}
