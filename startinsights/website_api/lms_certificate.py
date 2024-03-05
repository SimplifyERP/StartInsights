import frappe
from urllib.parse import urlencode
from frappe.utils.pdf import get_pdf
from startinsights.custom import get_domain_name



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


import requests
from frappe.utils import get_url

def get_pdf_certificate():
    host = "127.0.0.1:8001"
    doctype='LMS Certificate'
    docname='63af5bb7f9'
    print_format ='Certificate'
    url = f"http://{host}/api/method/frappe.utils.print_format.download_pdf?doctype={doctype}&name={docname}&format={print_format}&no_letterhead=0"
    api_key = 'a0fa6adb065d5c8'
    api_secret = '585dcbd321e73ec'
    header = {"Authorization": "token {}:{}".format(api_key, api_secret)}
    res = requests.get(url, headers=header, verify=False)
    print(res)
    with open(f'{doctype}-{docname}-{print_format}.pdf', 'wb') as f:
        f.write(res.content)
        print(res.content)

    file_name_inside = f"{docname}.pdf"
    new_file_inside = frappe.new_doc('File')
    new_file_inside.file_name = file_name_inside
    new_file_inside.attached_to_doctype = "Profile Application"
    new_file_inside.attached_to_name = docname
    new_file_inside.file_url = "/" + f'{doctype}-{docname}-{print_format}.pdf'
    new_file_inside.is_private = 0
    new_file_inside.save(ignore_permissions=True)
    frappe.db.commit()    
    # file_doc = frappe.get_doc({
    #     "doctype": "File",
    #     "file_name": f"{docname}.pdf",
    #     "attached_to_doctype": "LMS Certificate",
    #     "attached_to_name": docname,
    #     "file_url": "/" + f'{doctype}-{docname}-{print_format}.pdf'
    # })
    # file_doc.insert(ignore_permissions=True)
    
    # frappe.db.commit()    