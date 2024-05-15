import frappe

#user_type list view
@frappe.whitelist()
def get_masters():
    try:
        masters_data_list = {
            "countries":get_territory(),
        }
        return {"status": True, "masters_data": masters_data_list}
    except:
        return {"status": False}


# the below method is Investors Masters(territory,funding stages)  
def get_territory():
    territory = []
    get_territory_list = frappe.db.get_all("Territory",['name as country_name'])
    if get_territory_list:
        territory = get_territory_list
    else:
        territory = []
    return territory

def get_funding_stages():
    funding_stages = []
    get_funding_stages_list = frappe.db.get_all("Funding Stages",{'disabled':0},['name as funding_stage_name'])
    if get_funding_stages_list:
        funding_stages = get_funding_stages_list
    else:
        funding_stages = []
    return funding_stages       

@frappe.whitelist()
def get_captable_masters():
    try:
        captable_masters = {
            "round_type_list":get_captable_round_type_masters(),
            "instrument_type_list":get_captable_instrument_masters(),
            "bridge_round_type_list":get_captable_bridge_round_type()
            }
        return {"status":True,"captable_masters":captable_masters}
    except Exception as e:
        return {"status":False,"message":e}

def get_captable_round_type_masters():
    captable_round_type = []
    get_round_type_masters = frappe.db.get_all("Captable Round Type",{"disabled":0},["round_type",],order_by="order_wise ASC")
    if get_round_type_masters:
        captable_round_type = get_round_type_masters
    else:
        captable_round_type = []
    return captable_round_type    

def get_captable_instrument_masters():
    instrument_type = []
    get_instrument_type_masters = frappe.db.get_all("Captable Instrument",{"disabled":0},["instrument"],order_by="order_wise ASC")
    if get_instrument_type_masters:
        instrument_type = get_instrument_type_masters
    else:
        instrument_type = []
    return instrument_type       

def get_captable_bridge_round_type():
    bridge_round_type = []
    get_bridge_round_type_masters = frappe.db.get_all("Captable Bridge Round Type",{"disabled":0},["bridge_round_series"])
    if get_bridge_round_type_masters:
        bridge_round_type = get_bridge_round_type_masters
    else:
        bridge_round_type = []
    return bridge_round_type        
 