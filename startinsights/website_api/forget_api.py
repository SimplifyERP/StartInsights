import frappe
from frappe.utils import now,getdate,today,format_date
from datetime import datetime
from frappe import _
import random
import string

# Function to generate a random password
# forget password code
# @frappe.whitelist()
# def forget_password(email):
# 	status = False  # Initialize status as False
# 	message = ""
# 	try:
# 		# Check if the user exists and is enabled
# 		get_user = frappe.db.exists('User', {'name': email, 'enabled': 1})
# 		if get_user:
# 			# Generate a new password
# 			new_password = generate_password()
# 			# Update the user's password
# 			user = frappe.get_doc('User', email)
# 			user.set('new_password', new_password)
# 			user.save(ignore_permissions=True)
# 			frappe.db.commit()
# 			# Send notification email to the user
# 			subject =  _("'Password Reset'")
# 			email_args = {
# 				"recipients": email,
# 				"subject": subject,
# 				"message": f'We received a request to reset your Start Insights password.Your new password is: {new_password}',
# 				"queue": "short",
# 				"timeout": 300,
# 			}
# 			frappe.enqueue(
# 				method=frappe.sendmail, is_async=True, **email_args
# 			)
# 			status = True
# 			message = "Password reset successful. Check your email for the new password."
# 		else:
# 			message = "User does not exist or is not enabled."
# 	except Exception as e:
# 		message = f"Error: {str(e)}"
# 	return {'status': status, 'message': message}

# #the below code is for generating a random password
# def generate_password(length=8):
# 	characters = string.ascii_letters
# 	return ''.join(random.choice(characters) for i in range(length))



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
			# Set new_password as auth_code in Profile Application Document
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
				"message": f'Your Authentication: {new_auth_code}',
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
	except Exception as e:
		message = f"Error: {str(e)}"
	return {'status': status, 'message': message}
def generate_auth_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


#new password generate and set in user and profile application auth_code empty
@frappe.whitelist()
def change_password(user_id, new_password, confirm_password, auth_code):
	try:
		get_user = frappe.db.exists('User', {'name': user_id, 'enabled': 1})
		if not get_user:
			return "User does not exist"
		# Check if the provided auth_code matches the one in Profile application Document
		profile = frappe.get_doc("Profile Application", {"user_id": user_id, "auth_code": auth_code})
		if not profile:
			return "Invalid user_id or auth_code"
		if new_password != confirm_password:
			return "New password and confirm password do not match"

		# Check if new_password has at least 8 characters
		if len(new_password) < 8:
			return "New password must be at least 8 characters long"
		# Change password in the User document
		user = frappe.get_doc("User", user_id)
		user.new_password = confirm_password
		user.save(ignore_permissions=True)
		frappe.db.commit()
		# Empty the auth_code field in the Profile document
		profile.auth_code = ""
		profile.save(ignore_permissions=True)
		frappe.db.commit()
		return {"status": True, "message": "Password changed successfully."}
	except Exception as e:
		frappe.log_error(f"Error occurred: {str(e)}", "change_password")
		return "An error occurred while changing password"


