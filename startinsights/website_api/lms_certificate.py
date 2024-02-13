import frappe
from urllib.parse import urlencode

# lms certificate details
@frappe.whitelist()
def lms_certificate(course, member):
    try:
        # Retrieve the name of the LMS Certificate document based on member identifier
        certificate_name = frappe.db.get_value('LMS Certificate', {'member': member,"course":course}, 'name')
        if certificate_name:
            certificate = frappe.get_doc('LMS Certificate', certificate_name)
            print_format = certificate.template
            url_params = {
                "doctype": "LMS Certificate",
                "name": certificate_name,
                "trigger_print": "1",
                "format": print_format,
                "no_letterhead": "0"
            }
            url = "/api/method/frappe.utils.print_format.download_pdf?" + urlencode(url_params)
            print("Generated URL:", url)  # Add debug print
            pdf_url = frappe.utils.get_url(url)
            formatted_lms_certificate_details = {
                'course': certificate.course,
                'member': certificate.member,
                'pdf_url': pdf_url
            }
            return {"status": True, "lms_certificate": formatted_lms_certificate_details}
        else:
            return {"status": False, "message": f"No LMS Certificate found for member: {member}"}
    except Exception as e:
        frappe.log_error(f"Error generating certificate: {e}")
        return {"status": False, "message": f"Error generating certificate: {e}"}
