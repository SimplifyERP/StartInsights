import frappe
from frappe.utils.password import check_password,get_decrypted_password
from frappe.utils import  get_url



@frappe.whitelist(allow_guest=True)
def user_login(username,password):
    status = ""
    message = ""
    image_url = ""
    try:
        user = frappe.get_doc("User", username)
        if user and check_password(user.name,password):
            if user.cover_image:
                image_url = get_url() + user.cover_image
            else:
                image_url = ""    
            user_deatils = {
                "user_name" : username,
                "full_name":user.full_name,
                "phone_no":user.phone or "",
                "user_email":user.email,
                "profile_image":image_url
            }
            status = True
            message = "Login Successfull"
            return {"status":status,"message":message,"userinfo":user_deatils}
    except Exception as e:
        status = False
        message = e
        return {"status":status,"message":message}    
