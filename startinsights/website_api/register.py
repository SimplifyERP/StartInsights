import frappe
from frappe.utils import now,getdate,today,format_date
from datetime import datetime


@frappe.whitelist()
def create_account_against_lead(full_name,mobile_no,email_id):
    message = ""
    status = ""
    user_details = []
    try:
        if not frappe.db.exists("User",{'name':email_id,'enabled':1}):
            new_user = frappe.new_doc("User")
            new_user.email = email_id
            new_user.first_name = full_name
            new_user.phone = mobile_no
            new_user.send_welcome_email = 0
            new_user.append('roles', {
                'role': "Lead User",
                'doctype': 'Has Role',
                'parentfield': 'roles',
                'parenttype': 'User',
                'idx': 0,
                'has_role': 1
            })
            new_user.save(ignore_permissions=True)
            frappe.db.commit()

            create_lead(full_name,mobile_no,new_user.email)

            get_user_details = frappe.get_doc("User",email_id)
            user_details = {
                "user_id":get_user_details.name,
                "full_name":get_user_details.first_name,
                "mobile_no":get_user_details.phone
            }
            status = True
        else:
            status = False
            message = "User Already Created"
        return {"status":status,"user_details":user_details or message}
    except Exception as e:
        return {"status":False,"message":e}

#the below method is to create a new lead against user 
def create_lead(full_name,mobile_no,email_id):
    get_lead = frappe.db.get_value("Lead",{'lead_owner':email_id},['name'])
    if not get_lead:
        new_lead = frappe.new_doc("Lead")
        new_lead.first_name = full_name
        new_lead.mobile_no = mobile_no
        new_lead.email_id = email_id
        new_lead.status = "Lead"
        new_lead.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("Lead",new_lead.name,'lead_owner',email_id)
        frappe.db.set_value("Lead",new_lead.name,'owner',email_id)
    else:
        message = "Already Lead Created for User"
        return message  

# Creating a new user in user list
@frappe.whitelist()
def create_register_account(user_id,user_type,password):
    user_details = []
    status = ""
    message = ""
    try:
        if frappe.db.exists("User",{'name':user_id,'enabled':1}):   
            get_user = frappe.get_doc("User",user_id)
            get_user.new_password = password
            get_user.append('roles', {
                'role': user_type,
                'doctype': 'Has Role',
                'parentfield': 'roles',
                'parenttype': 'User',
                'idx': 0,
                'has_role': 1
            })
            get_user.save(ignore_permissions=True)
            frappe.db.commit()
            
            if not frappe.db.exists("Profile Application",{'name':user_id}):
                new_profile = frappe.new_doc("Profile Application")
                new_profile.user_id = user_id
                new_profile.email_id = user_id
                new_profile.phone_no = get_user.phone
                new_profile.customer_group = user_type
                new_profile.save(ignore_permissions=True)
                frappe.db.commit()

                #set the customer group in lead doctype
                get_lead = frappe.db.get_value("Lead",{'lead_owner':user_id},['name'])
                if get_lead:
                    frappe.db.set_value("Lead",get_lead,'custom_customer_group',user_type)

            else:
                message = "Please Contact Support Team" 
            get_user_details = frappe.get_doc("User",user_id)
            profile_details = frappe.get_doc("Profile Application",new_profile.name)
            user_details = {
                "user_id":get_user_details.name,
                "full_name":get_user_details.first_name,
                "mobile_no":get_user_details.phone,
                "type_of_user":profile_details.customer_group
            }
            status = True
        else:
            status = False
            message = "Given User ID not Created"    
        return {'status': status,"user_details":user_details or message}
    except Exception as e:
        status = False
        return {'status': status, 'message': str(e)}
    

@frappe.whitelist()
def social_register_account_create():
    try:
        pass
    except Exception as e:
        return {"status":False,"message":e}