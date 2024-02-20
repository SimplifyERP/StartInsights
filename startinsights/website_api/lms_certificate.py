import frappe
from urllib.parse import urlencode

# lms certificate details
@frappe.whitelist()
def get_lms_certificate(course, member):
    try:
        certificate_name = frappe.db.get_value('LMS Certificate', {'member': member,"course":course}, 'name')
        if certificate_name:
            frappe.db.set_value("LMS Certificate",certificate_name,"custom_get_certificate",1)
            send_email_certificate(certificate_name)
            return {"status": True, "lms_certificate":"mail send"}
        else:
            return {"status": False, "message": f"No LMS Certificate found for member: {member}"}
    except Exception as e:
        frappe.log_error(f"Error generating certificate: {e}")
        return {"status": False, "message": f"Error generating certificate: {e}"}

#send email to member with attachement of certificate
def send_email_certificate(certificate_name):
    password = None
    get_lms_data = frappe.get_doc("LMS Certificate",{'name':certificate_name})
    frappe.sendmail(
        recipients = get_lms_data.member,
        subject = frappe.db.get_single_value("LMS Email Settings","email_subject"),
        message = frappe.db.get_single_value("LMS Email Settings","email_message"),
        attachments = [frappe.attach_print(get_lms_data.doctype, get_lms_data.name, file_name=get_lms_data.course, password=password)]
    )
