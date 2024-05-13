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
    try:
        captable_list = []
        get_management = frappe.db.get_all("Captable Management",{'user':user_id},['name'])
        get_captable_data = frappe.get_doc("Captable Management",get_management)
        formated_floor_rs = "{:,.0f}".format(get_captable_data.floor_rs)
        formated_ceiling_rs = "{:,.0f}".format(get_captable_data.ceiling_rs)
        formated_pre_money_valuation = "{:,.0f}".format(get_captable_data.pre_money_valuation)
        formated_amount_raised = "{:,.0f}".format(get_captable_data.amount_raised)
        formated_post_money_valuation = "{:,.0f}".format(get_captable_data.post_money_valuation)
        formated_dilution_for_the_round = "{:,.0f}".format(get_captable_data.dilution_for_the_round)
        captable_data = {
            "id":get_captable_data.name,
            "name":get_captable_data.name,
            "user":get_captable_data.user or "",
            "company":get_captable_data.company or "",
            "round_type":get_captable_data.round_type or "",
            "instrument":get_captable_data.instrument or "",
            "bridge_round_from":get_captable_data.bridge_round_from or "",
            "bridge_round_to":get_captable_data.bridge_round_to or "",
            "floor_rs":formated_floor_rs or 0,
            "ceiling_rs":formated_ceiling_rs or 0,
            "pre_money_valuation":formated_pre_money_valuation or 0,
            "amount_raised":formated_amount_raised or 0,
            "post_money_valuation":formated_post_money_valuation or 0,
            "dilution_for_the_round":formated_dilution_for_the_round + "%" or 0,
            "no_of_investor":int(get_captable_data.no_of_investor or 0),
            "investors":[]
        }
        get_investors_table = frappe.db.get_all("Investor Table",{"parent":get_captable_data.name},["investor_name","invested_amount","_shareholding","no_of_shares_alloted"],order_by='idx ASC')
        for investors in get_investors_table:
            formated_invested_amount = "{:,.0f}".format(investors.invested_amount)
            formated_shareholding = "{:,.0f}".format(investors.invested_amount)
            formated_no_of_shares_alloted = "{:,.0f}".format(investors.no_of_shares_alloted)
            captable_data["investors"].append({
                "investor_name":investors.investor_name or "",
                "invested_amount":formated_invested_amount or 0,
                "shareholding":formated_shareholding or 0,
                "no_of_shares_alloted":formated_no_of_shares_alloted or 0
            })
        captable_list.append(captable_data)
        return {"status":True,"captable_list":captable_list}
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
