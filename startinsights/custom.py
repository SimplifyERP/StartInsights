import frappe
from urllib.parse import quote,urlparse
from frappe.utils.pdf import get_pdf


def get_domain_name():
    url = "https://startinsights.ai."
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    return f"https://{domain_name}"


def get_certificate_pdf():
    get_print_format = frappe.db.get_value("Print Format",{"name":"Certificate"},["html"])
    pdf = get_pdf(get_print_format)
    file_name_inside = "certificate.pdf"
    new_file_inside = frappe.new_doc('File')
    new_file_inside.file_name = file_name_inside
    new_file_inside.content = pdf
    # new_file_inside.attached_to_doctype = "Pitch Room"
    # new_file_inside.attached_to_name = new_room.name
    # new_file_inside.attached_to_field = "cover_image"
    new_file_inside.is_private = 0
    new_file_inside.save(ignore_permissions=True)
    frappe.db.commit()
    return "success"