import frappe
import base64
from startinsights.custom import get_domain_name


@frappe.whitelist()
def update_profile(full_name,mobile_no,email_id,designation,company_name,linkedin,website,profile_image,password):
    try:
        profile_image_decode = base64.b64decode(profile_image)
        get_user = frappe.get_doc("User",{'name':email_id})
        get_user.first_name = full_name
        get_user.phone_no = mobile_no
        get_user.email = email_id
        get_user.profile_password = password
        get_user.save(ignore_permissions=True)
        frappe.db.commit()
        #getting the profile image as base64 and converted create in a file doctype for user doctype
        if profile_image:
            file_name_inside = f"{get_user.first_name.replace(' ', '_')}profile_image.png"
            new_file_inside = frappe.new_doc('File')
            new_file_inside.file_name = file_name_inside
            new_file_inside.content = profile_image_decode
            new_file_inside.attached_to_doctype = "User"
            new_file_inside.attached_to_name = get_user.name
            new_file_inside.attached_to_field = "user_image"
            new_file_inside.is_private = 0
            new_file_inside.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("User",get_user.name,'user_image',new_file_inside.file_url)
        #another update of Profile application
        get_profile = frappe.get_doc("Profile Application",email_id)
        get_profile.full_name = full_name
        get_profile.email_id = email_id
        get_profile.designation = designation
        get_profile.phone_no = mobile_no
        get_profile.company_name = company_name
        get_profile.linkedin = linkedin
        get_profile.website = website
        get_profile.profile_password = password
        get_profile.save(ignore_permissions=True)
        frappe.db.commit()
        #getting the profile image as base64 and converted create in a file doctype for Profile Application doctype
        if profile_image:
            file_name_inside = f"{get_profile.full_name.replace(' ', '_')}profile.png"
            new_file_inside = frappe.new_doc('File')
            new_file_inside.file_name = file_name_inside
            new_file_inside.content = profile_image_decode
            new_file_inside.attached_to_doctype = "Profile Application"
            new_file_inside.attached_to_name = get_profile.name
            new_file_inside.attached_to_field = "profile_image"
            new_file_inside.is_private = 0
            new_file_inside.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("Profile Application",get_profile.name,'profile_image',new_file_inside.file_url)
        #after getting the Profile Details updated in application and returning the data
        get_updated_profile_data = frappe.get_doc("Profile Application",email_id)
        if get_updated_profile_data.profile_image:
            image_url = get_domain_name() + get_updated_profile_data.profile_image
        else:
            image_url = ""  
        user_details = {
            "user_name": get_updated_profile_data.name,
            "full_name": get_updated_profile_data.full_name,
            "mobile_no": get_updated_profile_data.phone_no,
            "user_email": get_updated_profile_data.email_id,
            "company_name":get_updated_profile_data.company_name,
            "designation":get_updated_profile_data.designation or "",
            "linkedin":get_updated_profile_data.linkedin,
            "website":get_updated_profile_data.website,
            "profile_image":image_url or "",
            "role": get_updated_profile_data.customer_group ,
        }
        return {"status":True,"userinfo":user_details}
    except Exception as e:
        return {"status":False,"message":e}

@frappe.whitelist()
def get_profile_details(user_id):
    try:
        get_profile = frappe.get_doc("Profile Application",user_id)
        profile_details = {
            "id":get_profile.name,
            "name":get_profile.name,
            "full_name":get_profile.full_name,
            "phone_no":get_profile.phone_no,
            "email":get_profile.email_id,
            "company":get_profile.company_name,
            "linkedin":get_profile.linkedin,
            "profile_image":get_profile.profile_image,
            "website":get_profile.website,

        }
    except Exception as e:
        return {"status":False,"message":e}