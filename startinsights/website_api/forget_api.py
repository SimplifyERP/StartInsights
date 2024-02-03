import frappe
from frappe.utils import now,getdate,today,format_date
from datetime import datetime
from frappe import _
import random
import string

# Function to generate a random password
# forget password code
@frappe.whitelist()
def forget_password(email):
	status = False  # Initialize status as False
	message = ""
	try:
		# Check if the user exists and is enabled
		get_user = frappe.db.exists('User', {'name': email, 'enabled': 1})
		if get_user:
			# Generate a new password
			new_password = generate_password()
			# Update the user's password
			user = frappe.get_doc('User', email)
			user.set('new_password', new_password)
			user.save(ignore_permissions=True)
			frappe.db.commit()
			# Send notification email to the user
			subject =  _("'Password Reset'")
			email_args = {
				"recipients": email,
				"subject": subject,
				"message": f'We received a request to reset your Start Insights password.Your new password is: {new_password}',
				"queue": "short",
				"timeout": 300,
			}
			frappe.enqueue(
				method=frappe.sendmail, is_async=True, **email_args
			)
			status = True
			message = "Password reset successful. Check your email for the new password."
		else:
			message = "User does not exist or is not enabled."
	except Exception as e:
		message = f"Error: {str(e)}"
	return {'status': status, 'message': message}

#the below code is for generating a random password
def generate_password(length=8):
	characters = string.ascii_letters
	return ''.join(random.choice(characters) for i in range(length))

	
