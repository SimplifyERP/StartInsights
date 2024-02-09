import frappe
from datetime import datetime
from frappe.utils import now, getdate, today, format_date, nowdate, add_months, get_time
import base64

@frappe.whitelist()
def create_investorwise_overview_list(name, tag_name, date_of_allotment, invested_round, amount_invested, distinctive_share_no, shares_allotted, price_per_share, fully_diluted_shares,class_of_shares,folio_number,shareholding):
    status = "False"  
    message = ""
    try:
        allot_date = datetime.strptime(date_of_allotment, '%d-%m-%Y').strftime('%Y-%m-%d')
        investor = frappe.new_doc("Investor-wise Overview")
        certificate = base64.b64decode(investor.share_certificate)
        investor.name1 = name
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
        investor.share_certificate = certificate
        investor.save(ignore_permissions=True)
        frappe.db.commit()
        status = True
        message = "Investor-wise Overview"
    except Exception as e:
        message = str(e) 
    return {"status": status, "message": message}

