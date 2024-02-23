import frappe
from datetime import datetime
from frappe.utils import now, getdate, today, format_date, nowdate, add_months, get_time
import random
import html2text

#the below code is to show the form title names
@frappe.whitelist()
def round_wise_form_title():
    try:
        round_wise = {
            "title_name":"Name of the round",
            "title_round_type":"Round Type",
            "title_date":"Closing date of the Round",
            "title_description":"Description",
            "title_security":"Select Security Prefix",
            "title_amount":"Amount Raised",
            "title_price":"Price per share",
            "title_pre_money":"Pre-Money Valuation",
            "title_dilution":"Dilution for this round (%)",
            "title_user":"Creation Person ID",
        }
        return {"status":True,"round_wise":round_wise}
    except Exception as e:
        return {"status":False,"message":e} 

# after showing the title form name enter the values and create a new rounded wise overview document.
@frappe.whitelist()
def create_round_wise_overview(round_name,round_type,closing_date_of_the_round,description,select_security_prefix,
                                amount_raised,price_per_share,pre_money_valuation,dilution_for_this_round,user_id):
    try:
        closing_date = datetime.strptime(str(closing_date_of_the_round), "%d-%m-%Y").date()
        color_code = get_random_color_code()
        round = frappe.new_doc("Round-wise Overview")
        round.name_of_the_round = round_name
        round.round_type = round_type
        round.closing_date_of_the_round = closing_date 
        round.description = description
        round.select_security_prefix = select_security_prefix
        round.amount_raised = amount_raised
        round.price_per_share = price_per_share
        round.pre_money_valuation = pre_money_valuation
        round.dilution_for_this_round = dilution_for_this_round
        round.creation_person_id = user_id
        round.color_code = color_code
        round.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.db.set_value('Round-wise Overview',round.name,'owner',user_id)
        message = " successfully Created Round-wise Overview"
        return {"status": True, "message": message}
    except Exception as e:
        return {"status": False, "message": e}

#the below method is randomly creating the color code
def get_random_color_code():
    color = random.randrange(0, 2**24)
    hex_color = hex(color)
    return hex_color
