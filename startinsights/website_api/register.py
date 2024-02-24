import frappe
from frappe.utils import now,getdate,today,format_date
from datetime import datetime

# Creating a new user in user list
@frappe.whitelist()
def create_user(first_name,user_id,phone_no,login_type,user_type,password,linkedin,company_name):
    status = ""
    message = ""
    try:
        if not frappe.db.exists("User",{'name':user_id,'enabled':1}):   
            new_user = frappe.new_doc('User')
            new_user.first_name = first_name
            new_user.email = user_id
            new_user.new_password = password
            new_user.send_welcome_email = 0
            new_user.append('roles', {
                'role': user_type,
                'doctype': 'Has Role',
                'parentfield': 'roles',
                'parenttype': 'User',
                'idx': 0,
                'has_role': 1
            })
            new_user.save(ignore_permissions=True)
            frappe.db.commit()

            if not frappe.db.exists("Profile Application",{'name':user_id}):
                new_profile = frappe.new_doc("Profile Application")
                new_profile.user_id = user_id
                new_profile.full_name = first_name
                new_profile.email_id = user_id
                new_profile.phone_no = phone_no
                new_profile.linkedin = linkedin
                new_profile.company_name = company_name
                new_profile.login_type = login_type
                new_profile.customer_group = user_type
                new_profile.save(ignore_permissions=True)
                frappe.db.commit()
            else:
                message = "Please Contact Support Team" 

            status = True
            message = "New User has been Created"
        else:
            status = False
            message = "Already User has been Created"    
        return {'status': status,"message":message}
    except Exception as e:
        status = False
        return {'status': status, 'message': str(e)}