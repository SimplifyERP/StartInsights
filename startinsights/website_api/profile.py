import frappe
import base64


@frappe.whitelist()
def create_profile(user,user_name,mobile_no,linkedin,company_name,designation,image):
    try:
        decoded_image = base64.b64decode(image)
        if not frappe.db.exists("Profile Application",{'user':user}):
            new_profile = frappe.new_doc("Profile Application")
            new_profile.user = user
            new_profile.user_name = user_name
            new_profile.email_id = user
            new_profile.mobile_no = mobile_no
            new_profile.linkedin = linkedin
            new_profile.company_name = company_name
            new_profile.designation = designation
            new_profile.profile_image = image

    except Exception as e:
        pass