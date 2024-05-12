import frappe
from datetime import datetime
import random
import base64
from startinsights.custom import get_domain_name
from frappe.utils import now, getdate, today, format_date



@frappe.whitelist()
def create_captable_managment(user,round_type,bridge_round_from,bridge_round_to,instrument,floor_cn,ceiling_cn,pre_money_valuation,amount_raised,no_of_investors,investors):
    try:
        if int(no_of_investors) > 0:
            if round_type == "Bridge Round":
                if instrument == "CN":
                    new_captable = frappe.new_doc("Captable Management")
                    new_captable.user = user
                    new_captable.round_type = round_type
                    new_captable.bridge_round_from = bridge_round_from
                    new_captable.bridge_round_to = bridge_round_to
                    new_captable.instrument = instrument
                    new_captable.floor_rs = floor_cn
                    new_captable.ceiling_rs = ceiling_cn
                    new_captable.pre_money_valuation = pre_money_valuation
                    new_captable.amount_raised = amount_raised
                    new_captable.no_of_investor = no_of_investors
                    for invest in investors:
                        new_captable.append("investor_table",{
                            "investor_name":invest.get("investor_name"),
                            "invested_amount":invest.get("amount")
                        })
                    new_captable.save(ignore_permissions=True)
                    frappe.db.commit()
                else:
                    new_captable = frappe.new_doc("Captable Management")
                    new_captable.user = user
                    new_captable.round_type = round_type
                    new_captable.bridge_round_from = bridge_round_from
                    new_captable.bridge_round_to = bridge_round_to
                    new_captable.instrument = instrument
                    new_captable.pre_money_valuation = pre_money_valuation
                    new_captable.amount_raised = amount_raised
                    new_captable.no_of_investor = no_of_investors
                    for invest in investors:
                        new_captable.append("investor_table",{
                            "investor_name":invest.get("investor_name"),
                            "invested_amount":invest.get("amount")
                        })
                    new_captable.save(ignore_permissions=True)
                    frappe.db.commit() 
            else:
                new_captable = frappe.new_doc("Captable Management")
                new_captable.user = user    
                new_captable.round_type = round_type
                new_captable.instrument = instrument
                new_captable.pre_money_valuation = pre_money_valuation
                new_captable.amount_raised = amount_raised
                new_captable.no_of_investor = no_of_investors
                for invest in investors:
                    new_captable.append("investor_table",{
                        "investor_name":invest.get("investor_name"),
                        "invested_amount":invest.get("amount")
                    })
                new_captable.save(ignore_permissions=True)
                frappe.db.commit()
        else:
            if round_type == "Bridge Round":
                if instrument == "CN":
                    new_captable = frappe.new_doc("Captable Management")
                    new_captable.user = user
                    new_captable.round_type = round_type
                    new_captable.bridge_round_from = bridge_round_from
                    new_captable.bridge_round_to = bridge_round_to
                    new_captable.instrument = instrument
                    new_captable.floor_rs = floor_cn
                    new_captable.ceiling_rs = ceiling_cn
                    new_captable.pre_money_valuation = pre_money_valuation
                    new_captable.amount_raised = amount_raised
                    new_captable.no_of_investor = no_of_investors
                    new_captable.save(ignore_permissions=True)
                    frappe.db.commit()
                else:
                    new_captable = frappe.new_doc("Captable Management")
                    new_captable.user = user
                    new_captable.round_type = round_type
                    new_captable.bridge_round_from = bridge_round_from
                    new_captable.bridge_round_to = bridge_round_to
                    new_captable.instrument = instrument
                    new_captable.pre_money_valuation = pre_money_valuation
                    new_captable.amount_raised = amount_raised
                    new_captable.no_of_investor = no_of_investors
                    new_captable.save(ignore_permissions=True)
                    frappe.db.commit() 
            else:
                new_captable = frappe.new_doc("Captable Management")
                new_captable.user = user    
                new_captable.round_type = round_type
                new_captable.instrument = instrument
                new_captable.pre_money_valuation = pre_money_valuation
                new_captable.amount_raised = amount_raised
                new_captable.no_of_investor = no_of_investors
                new_captable.save(ignore_permissions=True)
                frappe.db.commit()               
        return {"status":True,"message":"Captable Created Successfully"}
    except Exception as e:
        return {"status":False,"message":e}
    
#the below method is randomly creating the color code
def get_random_color_code():
    color = random.randrange(0, 2**24)
    hex_color = hex(color)
    return hex_color


@frappe.whitelist()
def captable_management_list(user_id):
    image_url = ""
    investor_wise_list = []
    round_wise_list = []
    try:
        get_management = frappe.db.get_all("Captable Management",{'user':user_id},['*'])
        format_management = []
        format_round_wise = []
        for management in get_management:
            # checking whether the user id is created any document
            if management.user:
                #get the image to concendation in domain name
                if management.share_certificate:
                    image_url = get_domain_name() + management.share_certificate
                else:
                    image_url = ""    
                investor_wise_list = {
                    "investor_name":management.investor_name,
                    "tag_name":management.tag_name,
                    "date_of_allotment":format_date(management.date_of_allotment),
                    "round_name":management.round_name,
                    "amount_invested":management.amount_invested,
                    "distinctive_share_no":management.distinctive_share_no,
                    "share_certificate":image_url,
                    "shares_allotted":management.shares_allotted,
                    "price_per_share":management.price_per_share,
                    "fully_diluted_shares":management.fully_diluted_shares,
                    "class_of_shares":management.class_of_shares,
                    "folio_number":management.folio_number,
                    "shareholding":management._shareholding,
                }
                format_management.append(investor_wise_list)
                #the below to sum the amount invested amount
                amount_raised_sum = frappe.db.sql(""" select sum(amount_invested) as invest_amount from `tabCaptable Management` where round_name = '%s' and user = '%s' """%(management.round_name,user_id),as_dict=1)
                if amount_raised_sum:
                    amount_raised = amount_raised_sum[0].get('invest_amount', 0.0)
                else:
                    amount_raised = 0.0
                #round wise list view
                round_wise_list = {
                    "round_name":management.round_name,
                    "round_type":management.round_type,
                    "round_closing_date":management.closing_date_of_the_round,
                    "description":management.description,
                    "select_security_prefix":management.select_security_prefix,
                    "amount_raised":amount_raised,
                    "price_per_share":management.price_per_share,
                    "pre_money_valuation":management.pre_money_valuation,
                    "dilution_for_this_round_":management.dilution_for_this_round_
                }
                format_round_wise.append(round_wise_list)
            else:
                investor_wise_list = []  
                round_wise_list = []
        return {
            "status":True,"investor_wise":format_management,
            "round_wise":format_round_wise,
            "investor_wise_graph":get_investor_wise_graph(user_id),
            "round_wise_graph":get_round_wise_graph(user_id)}
    except Exception as e:
        return {"status":False,"message":e}

def get_investor_wise_graph(user_id):
    try:
        get_investor_wise_data = frappe.db.get_all("Captable Management",{'user':user_id},['investor_name','_shareholding','color_code'])
        formatted_investor_wise_graph = []
        for investor in get_investor_wise_data:
            investor_wise_graph = {
                "name":investor.investor_name,
                "percentage":(investor._shareholding or "0"),
                "color_code":investor.color_code
            }
            formatted_investor_wise_graph.append(investor_wise_graph)
        return formatted_investor_wise_graph
    except Exception as e:
        return {"status":False,"message":e}        

def get_round_wise_graph(user_id):
    try:
        get_round_wise_data = frappe.db.get_all("Captable Management",{'user':user_id},['round_name','dilution_for_this_round_','color_code'])
        formatted_round_wise_graph = []
        for round in get_round_wise_data:
            round_wise_graph = {
                "name":round.round_name,
                "percentage":(round.dilution_for_this_round_ or "0"),
                "color_code":round.color_code
            }
            formatted_round_wise_graph.append(round_wise_graph)
        return formatted_round_wise_graph
    except Exception as e:
        return {"status":False,"message":e}        
