
import frappe
from frappe.utils.password import check_password, get_decrypted_password
from frappe.utils import get_url
@frappe.whitelist(allow_guest=True)
def user_login(username, password):
    status = ""
    message = ""
    image_url = ""
    role = ""
    try:
        user = frappe.get_doc("User", username)
        login_type_doc = frappe.get_all("Login Type", filters={"user": user.name}, fields=["user_type"])
        if login_type_doc:
            role = login_type_doc[0].user_type
        if user and check_password(user.name, password):
            if user.cover_image:
                image_url = get_url() + user.cover_image
            else:
                image_url = ""    

            user_details = {
                "user_name": username,
                "full_name": user.full_name,
                "phone_no": user.phone or "",
                "user_email": user.email,
                "role": role ,
                "profile_image": image_url
            }
            status = True
            message = "Login Successful"
            return {"status": status, "message": message, "userinfo": user_details}
    except Exception as e:
        status = False
        message = str(e)
        return {"status": status, "message": message}    
