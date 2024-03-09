# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from frappe.model.document import Document

class InvestorApplication(Document):
    pass

@frappe.whitelist()
def send_verification_email(name, email_id):
    doc = frappe.get_doc("Investor Application", name)
    if not doc.verify_code_email_sent:
        doc.verify_code_email_sent = 1
        doc.save(ignore_permissions=True)
        subject = _("Account Verification Code")
        message = _("Dear Sir/Madam, \n\nThis is your account verification code for login")
        frappe.sendmail(recipients=[email_id], subject=subject, message=message)
        frappe.msgprint(_("Verification code email sent successfully"))
        return True
    else:
        frappe.msgprint(_("Verification code email has already been sent"))
        return False
