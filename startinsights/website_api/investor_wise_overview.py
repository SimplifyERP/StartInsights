
import frappe
from datetime import datetime
from frappe.utils import now, getdate, today, format_date, nowdate, add_months, get_time
import base64

@frappe.whitelist()
def create_investorwise_overview_list(name, attach, tag_name, date_of_allotment, invested_round, amount_invested, distinctive_share_no, shares_allotted, price_per_share, fully_diluted_shares, class_of_shares, folio_number, shareholding):
    status = ""  
    message = ""
    try:
        allot_date = datetime.strptime(date_of_allotment, '%d-%m-%Y').strftime('%Y-%m-%d')
        investor = frappe.new_doc("Investor-Wise Overview")
        certificate = base64.b64decode(attach)
        investor.investor_name = name
        investor.tag_name = tag_name
        investor.date_of_allotment = allot_date 
        investor.invested_round = invested_round
        investor.amount_invested = amount_invested
        investor.distinctive_share_no = distinctive_share_no
        investor.shares_allotted = shares_allotted
        investor.price_per_share = price_per_share
        investor.fully_diluted_shares = fully_diluted_shares
        investor.class_of_shares = class_of_shares
        investor.folio_number = folio_number
        investor._shareholding = shareholding
        investor.save(ignore_permissions=True)
        frappe.db.commit()
        
        #base64 to pdf attach
        file_name_inside = f"{investor.name.replace(' ', '_')}_image.pdf"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = certificate
        new_file_inside.attached_to_doctype = "Investor-Wise Overview"
        new_file_inside.attached_to_name = investor.name
        new_file_inside.attached_to_field = "share_certificate"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value('Investor-Wise Overview', investor.name, 'share_certificate', new_file_inside.file_url)

        status = True
        message = "Successfully Created Investor-wise Overview"
        return {"status": status, "message": message}

    except Exception as e:
        status = False
        message = str(e)
        return {"status": status, "message": message}

