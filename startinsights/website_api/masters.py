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
def get_round_type():
    try:
        round_type = frappe.db.get_all("Round Type",['round_type','description'])
        return {"status":True,"round_type":round_type}
    except Exception as e:
        return {"status":False,"message":e}
