import frappe
from datetime import datetime
from frappe.utils import now, getdate, today, format_date, nowdate, add_months, get_time

@frappe.whitelist()
def create_roundwise_overview_list(round_name, round_type, closing_date_of_the_round, description, select_security_prefix, amount_raised, price_per_share, pre_money_valuation, dilution_for_this_round):
    status = ""
    message = ""
    try:
        closing_date = datetime.strptime(closing_date_of_the_round, '%d-%m-%Y').strftime('%Y-%m-%d')
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
        round.save(ignore_permissions=True)
        frappe.db.commit()

        status = True
        message = "Round-wise Overview"
        return {"status": status, "message": message}
    except Exception as e:
        status = False
        message = str(e)
        return {"status": status, "message": message}
