import frappe
from datetime import datetime
import random
import base64
from startinsights.custom import get_domain_name
from frappe.utils import now, getdate, today, format_date



@frappe.whitelist()
def create_captable_managment(user,round_type,bridge_round_from,bridge_round_to,instrument,floor_cn,ceiling_cn,pre_money_valuation,amount_raised,no_of_investors,investors,no_of_founders,founders):
    try:
        captable_list = []
        if int(no_of_founders) > 0 and int(no_of_investors) > 0:
            new_captable = frappe.new_doc("Captable Management")
            new_captable.user = user
            new_captable.round_type = round_type
            new_captable.color_code = get_random_color_code()
            new_captable.instrument = instrument 
            if round_type == "Bridge Round":
                new_captable.bridge_round_from = bridge_round_from
                new_captable.bridge_round_to = bridge_round_to      
                if instrument == "CN":
                    new_captable.floor_rs = floor_cn
                    new_captable.ceiling_rs = ceiling_cn  
            new_captable.pre_money_valuation = pre_money_valuation
            new_captable.amount_raised = amount_raised
            new_captable.no_of_investor = no_of_investors
            for invest in investors:
                new_captable.append("investors_table", {
                    "investor_name": invest.get("investor_name"),
                    "invested_amount": invest.get("amount")
                })
            for founder in founders:    
                new_captable.append("founders_details_table",{
                    "founder_name":founder.get("founder_name"),
                    "amount":founder.get("amount")
                })
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
def captable_management_list(user_id,type_of_round):
    try:
        captable_list = []
        get_management = frappe.db.get_all("Captable Management",{'user':user_id},['*'])
        for management in get_management:
            formated_floor_rs = "{:,.0f}".format(management.floor_rs)
            formated_ceiling_rs = "{:,.0f}".format(management.ceiling_rs)
            formated_pre_money_valuation = "{:,.0f}".format(management.pre_money_valuation)
            formated_amount_raised = "{:,.0f}".format(management.amount_raised)
            formated_post_money_valuation = "{:,.0f}".format(management.post_money_valuation)
            formated_dilution_for_the_round = "{:,.0f}".format(management.dilution_for_the_round)
            captable_data = {
                "id":management.name,
                "name":management.name,
                "user":management.user or "",
                "company":management.company or "",
                "round_type":management.round_type or "",
                "instrument":management.instrument or "",
                "bridge_round_from":management.bridge_round_from or "",
                "bridge_round_to":management.bridge_round_to or "",
                "floor_rs":formated_floor_rs or 0,
                "ceiling_rs":formated_ceiling_rs or 0,
                "pre_money_valuation":formated_pre_money_valuation or 0,
                "amount_raised":formated_amount_raised or 0,
                "post_money_valuation":formated_post_money_valuation or 0,
                "dilution_for_the_round":formated_dilution_for_the_round + "%" or 0,
                "no_of_investor":int(management.no_of_investor or 0),
                "investors":[]
            }
            get_investors_table = frappe.db.get_all("Investor Table",{"parent":management.name},["investor_name","invested_amount","_shareholding","no_of_shares_alloted"],order_by='idx ASC')
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
        return {"status":True,"captable_list":captable_list,"graph_data":get_graph_data(user_id,type_of_round)}
    except Exception as e:
        return {"status":False,"message":e}

def get_graph_data(user_id,type_of_round):
    captable_list_graph = []
    if type_of_round != "":
        get_captable_management = frappe.db.get_all("Captable Management",{'user':user_id},["name","round_type","color_code"])
        for captable in get_captable_management:
            if captable.round_type == type_of_round:
                get_investors_table = frappe.db.get_all("Investor Table",{"parent":captable.name},["investor_name","invested_amount","_shareholding","no_of_shares_alloted"],order_by='idx ASC')
                for investors in get_investors_table:
                    formated_invested_amount = "{:,.0f}".format(investors.invested_amount)
                    formated_shareholding = "{:,.0f}".format(investors.invested_amount)
                    formated_no_of_shares_alloted = "{:,.0f}".format(investors.no_of_shares_alloted)
                    captable_data = {
                        "color_code":captable.color_code or "",
                        "investor_name":investors.investor_name or "",
                        "invested_amount":formated_invested_amount or 0,
                        "shareholding":formated_shareholding or 0,
                        "no_of_shares_alloted":formated_no_of_shares_alloted or 0
                    }
                    captable_list_graph.append(captable_data)
    else:
        get_captable_management = frappe.db.get_value("Captable Management",{'round_type':"Seed"},["name","user","round_type","color_code"])
        if get_captable_management:
            if get_captable_management[1] == user_id:
                get_investors_table = frappe.db.get_all("Investor Table",{"parent":get_captable_management[0]},["investor_name","invested_amount","_shareholding","no_of_shares_alloted"],order_by='idx ASC')
                for investors in get_investors_table:
                    formated_invested_amount = "{:,.0f}".format(investors.invested_amount)
                    formated_shareholding = "{:,.0f}".format(investors.invested_amount)
                    formated_no_of_shares_alloted = "{:,.0f}".format(investors.no_of_shares_alloted)
                    captable_data = {
                        "color_code":get_captable_management[3] or "",
                        "investor_name":investors.investor_name or "",
                        "invested_amount":formated_invested_amount or 0,
                        "shareholding":formated_shareholding or 0,
                        "no_of_shares_alloted":formated_no_of_shares_alloted or 0
                    }
                    captable_list_graph.append(captable_data)
            else:
                captable_list_graph = []
        else:
            captable_list_graph = []        
    return captable_list_graph
   