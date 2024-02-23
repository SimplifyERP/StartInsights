import frappe
from frappe.utils import  get_url



@frappe.whitelist()
def get_investor_round_wise_details(user_id):
    try:
       investor_wise_list = get_investor_wise_list_view(user_id)
       investor_wise_graph = get_investor_wise_graph(user_id)
       round_wise_list = get_round_wise_list_view(user_id)
       round_wise_graph = get_round_wise_graph(user_id)
       return {
           "status":True,
           "investor_wise_list":investor_wise_list,
           "investor_wise_graph":investor_wise_graph,
           "round_wise_list":round_wise_list,
           "round_wise_graph":round_wise_graph
           }
    except Exception as e:
        pass


def get_investor_wise_list_view(user_id):
    try:
        get_investor_wise = frappe.db.get_all("Investor-Wise Overview",{'creation_person_id':user_id},['*']) 
        formatted_investor_wise= [] 
        for investor in get_investor_wise:
            if investor.share_certificate:
                attach = get_url + investor.share_certificate
            else:
                attach = ""    
            investor_wise = {
                "investor_name":investor.investor_name,
                "tag_name":investor.tag_name,
                "date_of_allotment":investor.date_of_allotment,
                "invested_round":investor.invested_round,
                "amount_invested":investor.amount_invested,
                "distinctive_share_no":investor.distinctive_share_no,
                "share_certificate":attach,
                "shares_allotted":investor.shares_allotted,
                "price_per_share":investor.price_per_share,
                "fully_diluted_shares":investor.fully_diluted_shares,
                "class_of_shares":investor.class_of_shares,
                "folio_number":investor.folio_number,
                "shareholding":investor._shareholding,
                "creation_person_id":investor.creation_person_id
            }
            formatted_investor_wise.append(investor_wise)
        return formatted_investor_wise
    except Exception as e:
        return {"status":False,"message":e} 
    
def get_investor_wise_graph(user_id):
    try:
        get_investor_wise_data = frappe.db.get_all("Investor-Wise Overview",{'creation_person_id':user_id},['investor_name','_shareholding','color_code'])
        formatted_investor_wise_graph = []
        for investor in get_investor_wise_data:
            investor_wise_graph = {
                "name":investor.investor_name,
                "percentage":investor._shareholding,
                "color_code":investor.color_code
            }
            formatted_investor_wise_graph.append(investor_wise_graph)
        return formatted_investor_wise_graph
    except Exception as e:
        return {"status":False,"message":e}        

def get_round_wise_list_view(user_id):
    try:
        get_round_wise = frappe.db.get_all("Round-wise Overview",{'creation_person_id':user_id},['*']) 
        formatted_round_wise= [] 
        for round_wise in get_round_wise:
            round_wise = {
                "name_of_the_round":round_wise.name_of_the_round,
                "round_type":round_wise.round_type,
                "closing_date_of_the_round":round_wise.closing_date_of_the_round,
                "description":round_wise.description,
                "select_security_prefix":round_wise.select_security_prefix,
                "amount_raised":round_wise.amount_raised,
                "price_per_share":round_wise.price_per_share,
                "pre_money_valuation":round_wise.pre_money_valuation,
                "dilution_for_this_round":round_wise.dilution_for_this_round,
                "creation_person_id":round_wise.creation_person_id
            }
            formatted_round_wise.append(round_wise)
        return formatted_round_wise 
    except Exception as e:
        return {"status":False,"message":e}     

def get_round_wise_graph(user_id):
    try:
        get_round_wise_data = frappe.db.get_all("Round-wise Overview",{'creation_person_id':user_id},['name_of_the_round','dilution_for_this_round','color_code'])
        formatted_round_wise_graph = []
        for round in get_round_wise_data:
            round_wise_graph = {
                "name":round.name_of_the_round,
                "percentage":round.dilution_for_this_round,
                "color_code":round.color_code
            }
            formatted_round_wise_graph.append(round_wise_graph)
        return formatted_round_wise_graph
    except Exception as e:
        return {"status":False,"message":e}    