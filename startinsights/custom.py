import frappe
from urllib.parse import quote,urlparse
from frappe.utils.pdf import get_pdf


def get_domain_name():
    url = "https://startinsights.ai."
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    return f"https://{domain_name}"



@frappe.whitelist()
def generate_and_attach_certificate():
    get_certificate = frappe.get_doc("LMS Certificate","63af5bb7f9")
    pdf_content = frappe.get_print("LMS Certificate", get_certificate.name, as_pdf=True)
    file_name_inside = "certificate.pdf"
    new_file_inside = frappe.new_doc('File')
    new_file_inside.file_name = file_name_inside
    new_file_inside.content = pdf_content
    new_file_inside.attached_to_doctype = "User Created Investors"
    new_file_inside.attached_to_name = get_certificate.name
    # new_file_inside.attached_to_field = "investor_logo"
    new_file_inside.is_private = 0
    new_file_inside.save(ignore_permissions=True)
    frappe.db.commit()
    return "success"