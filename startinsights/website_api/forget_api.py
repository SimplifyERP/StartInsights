import frappe
from frappe.utils import now,getdate,today,format_date
from datetime import datetime
from frappe import _
import random
import string

# authcode generate in peofile application and send mail
@frappe.whitelist()
def auth_code_with_mail(email):
	status = False
	message = ""
	try:
		# Check if the user exists and is enabled
		get_user = frappe.db.exists('User', {'name': email, 'enabled': 1})
		if get_user:
			new_auth_code = generate_auth_code()

			# Set auth_code in Profile Application
			profile_doc = frappe.get_doc("Profile Application", {"user_id": email})
			if profile_doc:
				profile_doc.auth_code = new_auth_code
				profile_doc.save(ignore_permissions=True)
				frappe.db.commit()

			# Send notification email to the user
			subject = _("'Authentication Code and URL'")
			email_args = {
				"recipients": email,
				"subject": subject,
				"message": f'Your Authentication: {new_auth_code}<br> Please click the link to reset the password http://localhost:55395/ResetPassword',
				"queue": "short",
				"timeout": 300,
			}
			frappe.enqueue(
				method=frappe.sendmail, is_async=True, **email_args
			)
			status = True
			message = "Authentication Code and url is send to email, please confirm"
		else:
			message = "User does not exist or is not enabled."
		return {"status":status,"message":message}	
	except Exception as e:
		return {'status': False,'message':e}

#the below method is generating the auth code to set in profile application
def generate_auth_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

#new password generate and set in user and profile application auth_code empty
@frappe.whitelist()
def change_password(user_id,password,auth_code):
	status = ""
	message = ""
	try:
		get_user = frappe.db.exists('User', {'name': user_id, 'enabled': 1})
		if get_user:
		# Check if the provided auth_code matches the one in Profile application Document
			profile = frappe.get_doc("Profile Application", {"name": user_id})
			if profile:
				if auth_code == profile.auth_code:
					frappe.db.set_value("Profile Application",profile.name,"profile_password",password)
					frappe.db.set_value("User",user_id,"new_password",password)
					frappe.db.set_value("Profile Application",profile.name,"auth_code","")
					status = True
					message = "Password Reset Successfully"
				else:
					status = False
					message = "Give Auth Code is Not Validate"	
			else:
				status = False
				message = "Profile Not Created"
		else:
			status = False
			message = "User Not Created"				
		return {"status":status,"message":message}
	except Exception as e:
		return {"status":False,"message":e}

