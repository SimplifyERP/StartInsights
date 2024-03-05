import frappe
from frappe.utils import now, getdate, today, format_date
from datetime import datetime
import html2text
from frappe.utils import  get_url
from startinsights.custom import get_domain_name


# pitch craft service details view
@frappe.whitelist()
def pitch_craft_list(user_id):
	image_url = ""
	plain_text_short_description = ""
	try:
		pitch_craft_list = frappe.db.get_all('Pitch Craft',{'disabled':0},['name','service_name','pricing','short_description','pitch_craft_image'],order_by='idx ASC')
		formatted_pitch_craft_list = []
		for pitch_craft in pitch_craft_list:
			plain_text_short_description = html2text.html2text(pitch_craft.short_description).strip()
			if pitch_craft.pitch_craft_image:
				image_url = get_domain_name() + pitch_craft.pitch_craft_image
			else:
				image_url = ""    
			pitch_craft_details = {
				'id': pitch_craft.name,
				'service_name': pitch_craft.service_name,
				"pitch_craft_image":image_url,
				'pricing': pitch_craft.pricing,
				'short_description': plain_text_short_description,
			}
			formatted_pitch_craft_list.append(pitch_craft_details)
		my_services = get_my_services_pitch_craft(user_id)    
		return {"status": True, "services_list": formatted_pitch_craft_list,"my_services":my_services}
	except Exception as e:
		return {"status": False, "message": str(e)}


def get_my_services_pitch_craft(user_id):
	image_url = ""
	plain_text_short_description = ""
	try:
		pitch_craft_list = frappe.db.get_all('Pitch Craft Payment',{'login_user':user_id,'my_service_status':"Saved"},['name','pitch_craft_id'],order_by='idx ASC')
		formatted_pitch_craft_list = []
		for pitch_craft in pitch_craft_list:
			get_pitch_craft_details = frappe.get_doc("Pitch Craft",pitch_craft.pitch_craft_id)
			plain_text_short_description = html2text.html2text(get_pitch_craft_details.short_description).strip()
			if pitch_craft.pitch_craft_image:
				image_url = get_domain_name() + get_pitch_craft_details.pitch_craft_image
			else:
				image_url = ""    
			pitch_craft_details = {
				'id': pitch_craft.pitch_craft_id,
				'service_name': get_pitch_craft_details.service_name,
				"pitch_craft_image":image_url,
				'pricing': get_pitch_craft_details.pricing,
				'short_description': plain_text_short_description,
			}
			formatted_pitch_craft_list.append(pitch_craft_details)
		return formatted_pitch_craft_list
	except Exception as e:
		return {"message": str(e)}  
	

# pitch craft overview details
@frappe.whitelist()
def pitch_craft_overview_details(name):
	plain_text_short_description = ""
	plain_text_benefits = ""
	image_url = ""
	try:
		pitch_craft = frappe.get_doc('Pitch Craft', name)
		if not pitch_craft:
			return {"status": False, "message": f"Pitch Craft '{name}' not found"}
		plain_text_short_description = html2text.html2text(pitch_craft.description).strip()
		plain_text_benefits = html2text.html2text(pitch_craft.benefits).strip()
		if pitch_craft.pitch_craft_image:
			image_url = get_domain_name() + pitch_craft.pitch_craft_image
		else:
			image_url = ""    
		formatted_pitch_craft_details = {
			'id': pitch_craft.name,
			'service_name': pitch_craft.service_name,
			"pitch_craft_image":image_url,
			'pricing': pitch_craft.pricing,
			'benefits': plain_text_benefits,
			'description': plain_text_short_description,
		}
		return {"status": True, "pitch_craft_overview_details": formatted_pitch_craft_details}
	except:
		return {"status": False}

# pitch craft process & document details
@frappe.whitelist()
def pitch_craft_process_details(name):
	plain_text_deliverables = ""
	image_url = ""
	try:
		pitch_craft = frappe.get_doc('Pitch Craft', name)
		pitch_craft_list = []
		if not pitch_craft:
			return {"status": False, "message": f"Pitch Craft '{name}' not found"}
		plain_text_deliverables = html2text.html2text(pitch_craft.deliverables).strip()
		if pitch_craft.pitch_craft_image:
			image_url = get_domain_name() + pitch_craft.pitch_craft_image
		else:
			image_url = "" 
		pitch_craft_details = {
			'id': pitch_craft.name,
			'service_name': pitch_craft.service_name,
			"pitch_craft_image":image_url,
			'pricing': pitch_craft.pricing,
			'deliverables': plain_text_deliverables,
			'documents_required':[],
		}
		documents_required = frappe.db.get_all("Pitch Craft Documents Table",{'parent':name},['documents_required'],order_by='idx ASC')
		for documents in documents_required:
			pitch_craft_details['documents_required'].append({
				"documents":documents.documents_required
			})
		pitch_craft_list.append(pitch_craft_details)    
		return {"status": True, "pitch_craft_process_details": pitch_craft_list}
	except:
		return {"status": False}

# pitch craft full details
@frappe.whitelist()
def pitch_craft_service_details(name):
	plain_text_short_description = ""
	plain_text_benefits = ""
	plain_text_deliverables = ""
	image_url = ""
	try:
		pitch_craft = frappe.get_doc('Pitch Craft', name)
		pitch_craft_list = []
		if not pitch_craft:
			return {"status": False, "message": f"Pitch Craft '{name}' not found"}
		plain_text_short_description = html2text.html2text(pitch_craft.description).strip()
		plain_text_benefits = html2text.html2text(pitch_craft.benefits).strip()
		plain_text_deliverables = html2text.html2text(pitch_craft.deliverables).strip()
		if pitch_craft.pitch_craft_image:
			image_url = get_domain_name()+ pitch_craft.pitch_craft_image
		else:
			image_url = ""    
		pitch_craft_details = {
			'id': pitch_craft.name,
			'service_name': pitch_craft.service_name,
			"pitch_craft_image":image_url,
			'pricing': pitch_craft.pricing,
			'benefits': plain_text_benefits,
			'description': plain_text_short_description,
			'deliverables': plain_text_deliverables,
			'documents_required':[],
		}
		documents_required = frappe.db.get_all("Pitch Craft Documents Table",{'parent':name},['documents_required'],order_by='idx ASC')
		for documents in documents_required:
			pitch_craft_details['documents_required'].append({
				"documents":documents.documents_required
			})
		pitch_craft_list.append(pitch_craft_details)    
		return {"status": True, "pitch_craft_service_details": pitch_craft_list}
	except:
		return {"status": False}
	
@frappe.whitelist()
def make_pitch_craft_payment(pitch_craft_id,user,payment_id,amount, date):
	try:
		service_booked_date = datetime.strptime(date, "%d-%m-%Y").date()

		new_pitch_craft_payment = frappe.new_doc("Pitch Craft Payment")
		new_pitch_craft_payment.pitch_craft_id = pitch_craft_id
		new_pitch_craft_payment.service_booked_date = service_booked_date
		new_pitch_craft_payment.payment_status = "Paid"
		new_pitch_craft_payment.my_service_status = "Saved"
		new_pitch_craft_payment.payment_id = payment_id
		new_pitch_craft_payment.amount = amount
		new_pitch_craft_payment.login_user = user
		new_pitch_craft_payment.save(ignore_permissions=True)

		new_pitch_craft_doc_app = frappe.new_doc("Pitch Craft Documents Application")
		new_pitch_craft_doc_app.pitch_craft_service = pitch_craft_id
		new_pitch_craft_doc_app.pitch_craft_payment_id = new_pitch_craft_payment.name
		new_pitch_craft_doc_app.date = service_booked_date
		new_pitch_craft_doc_app.user = user
		new_pitch_craft_doc_app.save(ignore_permissions=True)

		new_pitch_craft_payment.submit()
		frappe.db.commit()

		return {"status": True, "message": "New Pitch Craft Payment Submitted"}
	except Exception as e:
		return {"status": False, "message": str(e)}

@frappe.whitelist()
def get_pitch_craft_payment_details(user_id,pitch_craft_id):
	try:
		get_payment_details = frappe.db.get_all("Pitch Craft Payment",{'login_user':user_id,'pitch_craft_id':pitch_craft_id},['name','payment_id','service_booked_date','amount'],order_by='idx ASC')
		format_payment = []
		for payment in get_payment_details:
			pitch_craft_payment_details = {
				"id":payment.name,
				"payment_id":payment.payment_id,
				"payment_date":format_date(payment.service_booked_date),
				"amount_paid":payment.amount,
			}
			format_payment.append(pitch_craft_payment_details)
		return {"status":True,"pitch_craft_payment_details":format_payment}    
	except Exception as e:
		return {"status":False,"message":e}
	

	