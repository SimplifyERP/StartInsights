import frappe

#user_type list view
@frappe.whitelist()
def get_masters():
    try:
        get_user_type_data = get_user_type()
        masters_data_list = {
            "user_type":get_user_type_data
        }
        return {"status": True, "masters_data": masters_data_list}
    except:
        return {"status": False}

#get the user type
def get_user_type():
    user_type = frappe.db.get_all('Start Insight User',['name'])
    return user_type
    
#the below api for round-wise overview field round type of master data
@frappe.whitelist()
def get_captable_masters():
    try:
        captable_masters = {
            "round_type_masters":get_round_type_masters(),
            "tag_name_masters":get_tag_name_masters(),
            "invested_round_masters":get_invested_round_masters()
        }
        return {"status":True,"captable_masters":captable_masters}
    except Exception as e:
        return {"status":False,"message":e}


def get_round_type_masters():
    round_type_masters = []
    round_type = frappe.db.get_all("Round Type",['round_type','description'])
    if round_type:
        round_type_masters = round_type
    else:
        round_type_masters = []
    return round_type_masters       

def get_tag_name_masters():
    tag_name_masters = []
    tag_name = frappe.db.get_all("Tag Name",['tag_name'])
    if tag_name:
        tag_name_masters = tag_name
    else:
        tag_name_masters = []
    return tag_name_masters    

def get_invested_round_masters():
    invested_round_masters = []
    invested_round = frappe.db.get_all("Invested Round",['invested_round'])
    if invested_round:
        invested_round_masters = invested_round
    else:
        invested_round_masters = []
    return invested_round_masters    

