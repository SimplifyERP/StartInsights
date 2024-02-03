import frappe
from frappe.utils import now, getdate, today, format_date
from datetime import datetime
from frappe import _


# Function to send quiz submission email
@frappe.whitelist()
def send_quiz_submission_email(email):
    status = False
    message = ""
    try:
        # Send quiz submission notification email to the provided email address
        subject = _("Quiz Submission Confirmation")
        email_args = {
            "recipients": email,
            "subject": subject,
            "message": "Thank you for submitting the quiz. Your submission has been received.",
            "queue": "short",
            "timeout": 300,
        }
        frappe.enqueue(
            method=frappe.sendmail, is_async=True, **email_args
        )
        status = True
        message = "Quiz submission email sent successfully."
    except Exception as e:
        message = f"Error: {str(e)}"
    return {'status': status, 'message': message}
