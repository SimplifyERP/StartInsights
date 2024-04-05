import frappe
from frappe.utils import now,getdate,today,format_date
from datetime import datetime
import random
import string


@frappe.whitelist()
def create_lead(full_name,last_name,mobile_no,email_id):
    status = ""
    message = ""
    user_details = []
    try:
        if not frappe.db.exists("Lead",{'email_id':email_id}):
            new_lead = frappe.new_doc("Lead")
            new_lead.email_id = email_id
            new_lead.first_name = full_name
            new_lead.last_name = last_name
            new_lead.mobile_no = mobile_no
            new_lead.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("Lead",new_lead.name,'owner',email_id)
            status = True
            message = "Success"
            #return the lead details
            get_lead = frappe.get_doc("Lead",new_lead.name)    
            user_details = {
                "full_name":get_lead.first_name,
                "mobile_no":get_lead.phone,
                "email_id":get_lead.email_id
            }
        else:
            status = False
            message = "Already Email ID in Lead"
        return {"status":status,"message":message,"user_details":user_details}
    except Exception as e:
        return {"status":False,"message":e}

# Creating a new user in user list
@frappe.whitelist()
def create_account(full_name,mobile_no,email_id,password,type_of_user):
    user_details = []
    status = ""
    message = ""
    try:
        if type_of_user == "Startups":
            # the below condition is update the user id for the goven details
            if not frappe.db.exists("User",{'name':email_id,'enabled':1}):   
                new_user = frappe.new_doc("User")
                new_user.email = email_id
                new_user.first_name = full_name
                new_user.phone = mobile_no
                new_user.new_password = password
                new_user.send_welcome_email = 0
                new_user.append('roles', {
                    'role': type_of_user,
                    'doctype': 'Has Role',
                    'parentfield': 'roles',
                    'parenttype': 'User',
                    'idx': 0,
                    'has_role': 1
                })
                new_user.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.db.set_value("User",new_user.name,'owner',email_id)
                #the below condition to check the already is profile application is created or not
                if not frappe.db.exists("Profile Application",{'name':email_id}):
                    new_profile = frappe.new_doc("Profile Application")
                    new_profile.user_id = email_id
                    new_profile.email_id = email_id
                    new_profile.phone_no = mobile_no
                    new_profile.customer_group = type_of_user
                    new_profile.profile_password = password
                    new_profile.save(ignore_permissions=True)
                    frappe.db.commit() 
                    frappe.db.set_value("Profile Application",new_profile.name,'owner',email_id)
                    #given the user details get in the User Doctype
                    get_user_details = frappe.get_doc("User",new_user.name)
                    #getting the profile related details
                    profile_details = frappe.get_doc("Profile Application",new_profile.name)
                    status = True  
                    user_details = {
                        "full_name":get_user_details.first_name,
                        "mobile_no":get_user_details.phone,
                        "email_id":get_user_details.name,
                        "type_of_user":profile_details.customer_group
                    } 
                else:
                    message = "Profile Application Already Created"        
            else:
                message = "Given User is Not Registered"
        else:
            create_investor_verify_code(full_name,email_id,type_of_user,mobile_no,password)
            get_investor_application = frappe.get_doc("Investor Application",{"email_id":email_id})
            status = True
            user_details = {
                "full_name":get_investor_application.full_name,
                "email_id":get_investor_application.email_id,
                "type_of_user":get_investor_application.type_of_user,
                "mobile_no":get_investor_application.mobile_no,
                "password":get_investor_application.password
            } 
        return {"status":status,"message":message,"user_details":user_details}
    except Exception as e:
        status = False
        return {'status': status, 'message': str(e)}

#create the investor type of user in investor appilcation for verify code creation
def create_investor_verify_code(full_name,email_id,type_of_user,mobile_no,password):
    verify_code_automatic = generate_verification_code(length=6)
    if not frappe.db.exists("Investor Application",{"email_id":email_id}):
        new_verify_code = frappe.new_doc("Investor Application")
        new_verify_code.email_id = email_id
        new_verify_code.full_name = full_name
        new_verify_code.type_of_user = type_of_user
        new_verify_code.verify_code = verify_code_automatic
        new_verify_code.mobile_no = mobile_no
        new_verify_code.password = password
        new_verify_code.verify_code_status = "Not In Use"
        new_verify_code.save(ignore_permissions=True)
        frappe.db.commit()
        message = "Code Created"
    else:
        message = "Already Email Exists"
    return message

#the below method is generating the verification code randomly
def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    verification_code = ''.join(random.choice(characters)for i in range(length))
    return verification_code

@frappe.whitelist()
def create_investors_account(verify_code,full_name,mobile_no,email_id,password,type_of_user):
    status = ""
    message = ""
    user_details = []
    try:
        get_investor_application = frappe.db.exists("Investor Application",{'email_id':email_id})
        if get_investor_application:
            get_verify_code = frappe.db.get_value("Investor Application",{'name':get_investor_application},['verify_code'])
            if get_verify_code == verify_code:
                #the below condition is get user and enabled
                if not frappe.db.exists("User",{'name':email_id,'enabled':1}):   
                    new_user = frappe.new_doc("User")
                    new_user.email = email_id
                    new_user.first_name = full_name
                    new_user.phone = mobile_no
                    new_user.new_password = password
                    new_user.send_welcome_email = 0
                    new_user.append('roles', {
                        'role': type_of_user,
                        'doctype': 'Has Role',
                        'parentfield': 'roles',
                        'parenttype': 'User',
                        'idx': 0,
                        'has_role': 1
                    })
                    new_user.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.set_value("User",new_user.name,'owner',email_id)
                    #after enabled the user creating the profile application against user
                    if not frappe.db.exists("Profile Application",{'name':email_id}):
                        new_profile = frappe.new_doc("Profile Application")
                        new_profile.user_id = email_id
                        new_profile.email_id = email_id
                        new_profile.phone_no = mobile_no
                        new_profile.customer_group = type_of_user
                        new_profile.profile_password = password
                        new_profile.save(ignore_permissions=True)
                        frappe.db.commit() 
                        frappe.db.set_value("Profile Application",new_profile.name,'owner',email_id)
                        frappe.db.set_value("Investor Application",email_id,"verify_code_status","Expired")
                        #given the user details get in the User Doctype
                        get_user_details = frappe.get_doc("User",new_user.name)
                        #getting the profile related details
                        profile_details = frappe.get_doc("Profile Application",new_profile.name)
                        status = True  
                        user_details = {
                            "full_name":get_user_details.first_name,
                            "mobile_no":get_user_details.phone,
                            "email_id":get_user_details.name,
                            "type_of_user":profile_details.customer_group
                        } 
                    else:
                        message = "Profile Application Already Created"  
                else:
                    message = "Given User is Not Registered"          
            else:
                message = "Given Verify Code is Wrong"
        else:
            message = "Given User Verify is Not Generated Contact Team"        
        return {"status":status,"message":message,"user_details":user_details}
    except Exception as e:
        return {"status":False,"message":e}
