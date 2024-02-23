import frappe
from datetime import datetime
from frappe.utils import now, getdate, today, format_date, nowdate, add_months, get_time
import base64
import random
from frappe.utils import  get_url
import html2text


@frappe.whitelist()
def investor_wise_form_title():
    try:
        investor_wise = {
            "title_name":"Investor Name",
            "title_tag":"Tag Name",
            "title_date":"Date of Allotment",
            "title_round":"Invested Round ",
            "title_amount":"Amount Invested",
            "title_distinctive":"Distinctive Share No",
            "title_share_certificate":"Share Certificate",
            "title_share_alloted":"Shares Allotted",
            "title_price":"Price Per Share",
            "title_fully_diluted_shares":"Fully Diluted Shares",
            "title_class_of_shares":"Class Of Shares",
            "title_folio_number":"Folio Number",
            "title_shareholding":"% Shareholding",
            "title_creation_person_id":"Creation Person ID"
        }
        return {"status":True,"investor_wise":investor_wise}
    except Exception as e:
        return {"status":False,"message":e} 

@frappe.whitelist()
def create_investor_wise_overview_list(name,attach,tag_name,date_of_allotment,invested_round,amount_invested,distinctive_share_no,
                                    shares_allotted,price_per_share,fully_diluted_shares,class_of_shares,folio_number,shareholding,user_id):
    try:
        allot_date = datetime.strptime(str(date_of_allotment), "%d-%m-%Y").date()
        certificate = base64.b64decode(attach)
        color_code = get_random_color_code()

        investor = frappe.new_doc("Investor-Wise Overview")
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
        investor.creation_person_id = user_id
        investor.color_code = color_code
        investor.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value('Investor-Wise Overview',investor.name,'owner',user_id)
        
        #base64 to pdf attach
        if certificate:
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

        message = "Successfully Created Investor-wise Overview"
        return {"status": True, "message": message}
    except Exception as e:
        return {"status": False, "message": e}

#the below method is randomly creating the color code
def get_random_color_code():
    color = random.randrange(0, 2**24)
    hex_color = hex(color)
    return hex_color