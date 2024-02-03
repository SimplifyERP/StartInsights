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