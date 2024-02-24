import frappe
from frappe.utils.password import check_password, get_decrypted_password
from frappe.utils import get_url

    
@frappe.whitelist(allow_guest=True)
def user_login(username, password):
    status = ""
    message = ""
    image_url = ""
    try:
        user = frappe.get_doc("User", username)
        if user.name:
            if user and check_password(user.name, password):
                profile = frappe.get_doc("Profile Application",username)
                if profile.profile_image:
                    image_url = get_url() + profile.profile_image
                else:
                    image_url = ""    

                user_details = {
                    "user_name": profile.user_id,
                    "full_name": profile.full_name,
                    "user_email": profile.email_id,
                    "company_name":profile.company_name,
                    "phone_no": profile.phone_no,
                    "designation":profile.designation or "",
                    "linkedin":profile.linkedin,
                    "profile_image":image_url or "",
                    "login_type":profile.login_type or "",
                    "role": profile.customer_group ,
                }
            else:
                message = "please contact support team" 
        else:
            message = "please contact support team"        
        status = True
        message = "Login Successful"
        return {"status": status, "message": message, "userinfo": user_details}
    except Exception as e:
        status = False
        message = str(e)
        return {"status": status, "message": message}    
