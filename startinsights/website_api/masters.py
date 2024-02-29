import frappe

#user_type list view
@frappe.whitelist()
def get_masters():
    try:
        masters_data_list = {
            "user_type": get_user_type(),
            "round_type_masters":get_round_type_masters(),
            "tag_name_masters":get_tag_name_masters(),
            "invested_round_masters":get_invested_round_masters(),
            "countries":get_territory(),
            "funding_stages":get_funding_stages()
        }
        return {"status": True, "masters_data": masters_data_list}
    except:
        return {"status": False}

#get the user type
def get_user_type():
    user_type = frappe.db.get_all('Start Insight User',['name'])
    return user_type

# the below method is capatable masters(round_type,tag_name,invested_round_masters)
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

# the below method is Investors Masters(territory,funding stages)  
def get_territory():
    territory = []
    get_territory_list = frappe.db.get_all("Territory",['name'])
    if get_territory_list:
        territory = get_territory_list
    else:
        territory = []
    return territory

def get_funding_stages():
    funding_stages = []
    get_funding_stages_list = frappe.db.get_all("Funding Stages",{'disabled':0},['name'])
    if get_funding_stages_list:
        funding_stages = get_funding_stages_list
    else:
        funding_stages = []
    return funding_stages        