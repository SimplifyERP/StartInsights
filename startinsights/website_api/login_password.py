import frappe


@frappe.whitelist()
def update_login_password(user_id,current_password,new_password):
    message = ""
    status = ""
    try:
        get_user = frappe.db.get_value("Profile Application",{'name':user_id},['profile_password'])
        if get_user == current_password:
            frappe.db.set_value("User",user_id,'new_password',new_password)
            frappe.db.set_value("Profile Application",user_id,"profile_password",new_password)
            status = True
            message = "New Password Has been Changed"
        else:
            status = False
            message = "Your Current Password is Wrong"    
        return {"status":status,"password_update":message}
    except Exception as e:
        return {"status":False,"message":e}