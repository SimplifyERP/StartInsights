import frappe
from frappe.utils import now, getdate, today, format_date
from datetime import datetime
import html2text
from frappe.utils import  get_url
from startinsights.custom import get_domain_name


# pitch craft service details view
@frappe.whitelist()
def service_list(user_id):
	purchase_status = False
	image_url = ""
	try:
		service_list = frappe.db.get_all('Services',{'disabled':0},["*"],order_by='idx ASC')
		service_list_format = []
		for service in service_list:
			get_purchase_service = frappe.db.get_value("Service Payment",{"login_user":user_id,"service_id":service.name},['name'])
			if get_purchase_service:
				purchase_status = True
			else:
				purchase_status = False	
			#the below format is giving the text editor field data removed html tags
			format_short_description = html2text.html2text(service.short_description).strip() or ""
			format_benefits = html2text.html2text(service.benefits).strip() or ""
			format_description = html2text.html2text(service.description).strip() or ""
			format_deliverables = html2text.html2text(service.deliverables).strip() or ""
			#added the domain name with image url
			if service.service_image:
				image_url = get_domain_name() + service.service_image
			else:
				image_url = ""    
			#response	
			service_details = {
				"id": service.name,
				"service_payment_id":"",
				'purchase_status':purchase_status,
				"service_name": service.service_name,
				"service_image":image_url,
				"pricing": service.pricing,
				"short_description": format_short_description,
				"benefits":format_benefits,
				"description":format_description,
				"deliverables":format_deliverables,
				"documents":[]
			}
			service_documents = frappe.db.get_all("Service Documents",{'parent':service.name},['documents_required'],order_by='idx ASC')
			for documents in service_documents:
				service_details['documents'].append({
					"documents":documents.documents_required
				})
			service_list_format.append(service_details) 
		my_services = get_my_services_list(user_id)    
		return {"status": True, "services_list": service_list_format,"my_services":my_services}
	except Exception as e:
		return {"status": False, "message": str(e)}

#by using this method for my service list for separate user
def get_my_services_list(user_id):
	format_short_description = ""
	format_benefits = ""
	format_description = ""
	format_deliverables = ""
	image_url = ""
	try:
		service_payment = frappe.db.get_all('Service Payment',{'login_user':user_id,'my_service_status':"Saved"},['name','service_id'],order_by='idx ASC')
		service_payment_list = []
		for payment in service_payment:
			#by passing the service id to get all service details
			service_details = frappe.get_doc("Services",payment.service_id)
			#by getting the text editor data to remove the html tags
			format_short_description = html2text.html2text(service_details.short_description).strip() or ""
			format_benefits = html2text.html2text(service_details.benefits).strip() or ""
			format_description = html2text.html2text(service_details.description).strip() or ""
			format_deliverables = html2text.html2text(service_details.deliverables).strip() or ""
			#by concedation the domain name and image url path to show image or anything
			if service_details.service_image:
				image_url = get_domain_name() + service_details.service_image
			else:
				image_url = ""    
			service_details = {
				"id": payment.service_id,
				"service_payment_id":payment.name,
				'purchase_status':True,
				"service_name": service_details.service_name,
				"service_image":image_url,
				"pricing": service_details.pricing,
				"short_description": format_short_description,
				"benefits":format_benefits,
				"description":format_description,
				"deliverables":format_deliverables,
				"documents":[]
			}
			service_documents = frappe.db.get_all("Service Documents",{'parent':payment.name},['documents_required'],order_by='idx ASC')
			for documents in service_documents:
				service_details['documents'].append({
					"documents":documents.documents_required
				})
			service_payment_list.append(service_details) 		
		return service_payment_list
	except Exception as e:
		return e
	
#the below is user get the service after payment creation
@frappe.whitelist()
def create_service_payment(service_id,user,payment_id,amount,date):
	try:
		service_date_format = datetime.strptime(date, "%d-%m-%Y").date()
		new_service_payment = frappe.new_doc("Service Payment")
		new_service_payment.service_id = service_id
		new_service_payment.service_booked_date = service_date_format
		new_service_payment.payment_status = "Paid"
		new_service_payment.my_service_status = "Saved"
		new_service_payment.payment_id = payment_id
		new_service_payment.amount = amount
		new_service_payment.login_user = user
		new_service_payment.save(ignore_permissions=True)
		frappe.db.commit()
		frappe.db.set_value("Service Payment",new_service_payment.name,'owner',user)
		return {"status": True, "message":"Service Payment Created"}
	except Exception as e:
		return {"status": False, "message": str(e)}

#the below method id get the service payment details
@frappe.whitelist()
def get_service_payment_details(user_id,payment_id):
	try:
		get_service_payment = frappe.db.get_all("Service Payment",{"name":payment_id,"login_user":user_id},['name','payment_id','service_booked_date','amount'],order_by='idx ASC')
		payment_list = []
		for payment in get_service_payment:
			service_payment_details = {
				"id":payment.name,
				"payment_id":payment.payment_id,
				"payment_date":format_date(payment.service_booked_date),
				"amount_paid":payment.amount,
			}
			payment_list.append(service_payment_details)
		return {"status":True,"service_payment_details":payment_list}    
	except Exception as e:
		return {"status":False,"message":e}
	

	