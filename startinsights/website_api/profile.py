import frappe
import base64
from startinsights.custom import get_domain_name


@frappe.whitelist()
def update_profile(user_id,full_name,email_id,phone_no,company_name,designation,linkedin,image,user_type):
    try:
        decode_image = base64.b64decode(image)
        get_user = frappe.get_doc("User",{'name':user_id})
        get_user.first_name = full_name
        get_user.username = full_name
        get_user.email = email_id
        get_user.save(ignore_permissions=True)
        frappe.db.commit()
        #the below code is set the profile application full name changed
        frappe.db.set_value("Profile Application",get_user.name,'full_name',full_name)
        
        file_name_inside = f"{get_user.first_name.replace(' ', '_')}document.png"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = decode_image
        new_file_inside.attached_to_doctype = "User"
        new_file_inside.attached_to_name = get_user.name
        new_file_inside.attached_to_field = "user_image"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.db.set_value("User",get_user.name,'user_image',new_file_inside.file_url)

        get_profile = frappe.get_doc("Profile Application",user_id)
        get_profile.email_id = email_id
        get_profile.company_name = company_name
        get_profile.phone_no = phone_no
        get_profile.designation = designation
        get_profile.linkedin = linkedin
        get_profile.customer_group = user_type
        get_profile.save(ignore_permissions=True)
        frappe.db.commit()

        file_name_inside = f"{get_profile.full_name.replace(' ', '_')}document.png"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = decode_image
        new_file_inside.attached_to_doctype = "Profile Application"
        new_file_inside.attached_to_name = get_profile.name
        new_file_inside.attached_to_field = "profile_image"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.db.set_value("Profile Application",get_profile.name,'profile_image',new_file_inside.file_url)

        if get_profile.profile_image:
            image_url = get_domain_name() + get_profile.profile_image
        else:
            image_url = ""    
        user_details = {
            "user_name": get_user.name,
            "full_name": get_user.full_name,
            "user_email": get_profile.email_id,
            "company_name":get_profile.company_name,
            "phone_no": get_profile.phone_no,
            "designation":get_profile.designation or "",
            "linkedin":get_profile.linkedin,
            "profile_image":image_url or "",
            "login_type":get_profile.login_type or "",
            "role": get_profile.customer_group ,
        }
        return {"status":True,"userinfo":user_details}
    except Exception as e:
        return {"status":False,"message":e}