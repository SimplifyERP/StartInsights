import frappe
from frappe.utils import now,getdate,today,format_date
from datetime import datetime

# Creating a new user in user list
@frappe.whitelist()
def create_user(user_id,password,user_type,first_name,phone_no,login_type):
    status = ""
    message = ""
    try:
        if not frappe.db.exists("User",{'name':user_id,'enabled':1}):
            new_user = frappe.new_doc('User')
            new_user.email = user_id
            new_user.first_name = first_name
            new_user.new_password = password
            new_user.phone = phone_no
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

            if not frappe.db.exists("Login Type",{'name':user_id}):
                new_login_user = frappe.new_doc('Login Type')
                new_login_user.user = user_id
                new_login_user.login_type = login_type
                new_login_user.user_type = user_type
                new_login_user.save(ignore_permissions=True)
                frappe.db.commit()
            else:
                message = "Login Type User Already Created"    

            status = True
            message = "New User has been Created"
        else:
            status = False
            message = "Already User has been Created"    
        return {'status': status,"message":message}
    except Exception as e:
        status = False
        return {'status': status, 'message': str(e)}