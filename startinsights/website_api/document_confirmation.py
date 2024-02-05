
import frappe
from frappe.utils import get_url


# Creating a document confirmation list
@frappe.whitelist()
def doc_confirmation(name,email,company):
    status = True
    message = "Document Confirmation Created"
    try:
        doc_confirmation = frappe.new_doc('Document Confirmation')
        doc_confirmation.name1 = name
        doc_confirmation.email = email
        doc_confirmation.company = company
        doc_confirmation.save(ignore_permissions=True)
        frappe.db.commit()

      
        return {'status': status,"message":message}
    except Exception as e:
        status = False
        return {'status': status, 'message': str(e)}
