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
	format_short_description = ""
	format_about_service = ""
	format_deliverables = ""
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
			format_short_description = html2text.html2text(service.short_description or "").strip() 
			format_about_service = html2text.html2text(service.about_service or "").strip() 
			format_deliverables = html2text.html2text(service.deliverables or "").strip() 
			#added the domain name with image url
			if service.service_image:
				image_url = get_domain_name() + service.service_image
			else:
				image_url = ""    
			#response	
			service_details = {
				"id": service.name,
				'purchase_status':purchase_status,
				"service_status":"",
				"service_name": service.service_name,
				"service_image":image_url,
				"pricing": service.pricing,
				"short_description": format_short_description,
				"about_service":format_about_service,
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
	format_about_service = ""
	format_deliverables = ""
	image_url = ""
	service_details = []
	try:
		my_services = frappe.db.get_all('My Services',{'user':user_id,'my_service_status':"Saved"},['name','service_id','service_status'],order_by='idx ASC')
		service_payment_list = []
		for service in my_services:
			#by passing the service id to get all service details
			service_detail = frappe.get_doc("Services",service.service_id)
			#by getting the text editor data to remove the html tags
			format_short_description = html2text.html2text(service_detail.short_description or "").strip() 
			format_about_service = html2text.html2text(service_detail.about_service or "").strip() 
			format_deliverables = html2text.html2text(service_detail.deliverables or "").strip() 
			#by concedation the domain name and image url path to show image or anything
			if service_detail.service_image:
				image_url = get_domain_name() + service_detail.service_image
			else:
				image_url = ""    
			service_details = {
				"id": service.name,
				'purchase_status':True,
				"service_status":service.service_status,
				"service_name": service_detail.service_name,
				"service_image":image_url,
				"pricing": service_detail.pricing,
				"short_description": format_short_description,
				"about_service":format_about_service,
				"deliverables":format_deliverables,
				"documents":[]
			}
			service_documents = frappe.db.get_all("Service Documents",{'parent':service.service_id},['documents_required'],order_by='idx ASC')
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
		new_service_payment.payment_id = payment_id
		new_service_payment.amount = amount
		new_service_payment.login_user = user
		new_service_payment.save(ignore_permissions=True)
		frappe.db.commit()
		frappe.db.set_value("Service Payment",new_service_payment.name,'owner',user)

		create_my_services(user,service_id,new_service_payment.name)

		return {"status": True, "message":"Service Payment Created"}
	except Exception as e:
		return {"status": False, "message": str(e)}

#create a my service list for user wise
def create_my_services(user,service_id,name):
	try:
		get_process = frappe.db.get_all("Process Steps",{"parent":service_id},['steps','tat','status'],order_by='idx ASC')
		my_service = frappe.new_doc("My Services")
		my_service.user = user
		my_service.service_id = service_id
		my_service.service_status = "Under Progress"
		my_service.service_payment_id = name
		my_service.my_service_status = "Saved"
		for service in get_process:
			my_service.append("process_steps",{
				"steps":service.get("steps"),
				"tat":service.get("tat"),
				"status":service.get("status")
			})
		my_service.save(ignore_permissions=True)
		frappe.db.commit()
		frappe.db.set_value("My Services",my_service.name,'owner',user)
		return {"status":True,"message":"My Service Created"}
	except Exception as e:
		return {"status":False,"message":e}
	
#getting the my service details
@frappe.whitelist()
def get_my_service_details(my_service_id):
	image_url = ""
	user_image = ""
	assigned_user = []
	payment_details = []
	process_status = False
	format_short_description = ""
	format_about_service = ""
	format_deliverables = ""
	try:
		my_service_list = []
		my_service = frappe.get_doc("My Services",my_service_id)
		get_master_services = frappe.get_doc("Services",my_service.service_id)
		if get_master_services.service_image:
				image_url = get_domain_name() + get_master_services.service_image
		else:
			image_url = ""    
		format_short_description = html2text.html2text(get_master_services.short_description or "").strip() 
		format_about_service = html2text.html2text(get_master_services.about_service or "").strip() 
		format_deliverables = html2text.html2text(get_master_services.deliverables or "").strip()
		my_service_details = {
			"id": my_service.name,
			'purchase_status':True,
			"service_name": get_master_services.service_name,
			"service_image":image_url,
			"pricing": get_master_services.pricing,
			"short_description": format_short_description,
			"about_service":format_about_service,
			"deliverables":format_deliverables,
			"documents":[],
			"service_status":my_service.service_status,
			"service_tracking":[]
		}
		service_documents = frappe.db.get_all("Service Documents",{'parent':get_master_services.name},['documents_required'],order_by='idx ASC')
		for documents in service_documents:
			my_service_details['documents'].append({
					"documents":documents.documents_required
				})
		my_service_documents = frappe.db.get_all("Process Steps",{'parent':my_service.name},['steps','tat','status'],order_by='idx ASC')
		for documents in my_service_documents:
			if documents.status == "Completed":
				process_status = True
			else:
				process_status = False	
			my_service_details["service_tracking"].append({
				"steps":documents.steps,
				"tat":documents.tat,
				"current_status":documents.status,
				"status":process_status
			})
		if my_service.assigned_user_image:
			user_image = get_domain_name() +  my_service.assigned_user_image
		else:
			user_image = ""	
		assigned_user = {
			"user_name":my_service.user_name or "",
			"designation":my_service.designation or "",
			"mobile_no":my_service.mobile_no or "",
			"image":user_image
		}	
		payment_details = get_service_payment_details(my_service.service_payment_id)			
		my_service_list.append(my_service_details)
		return {"status":True,"my_service_details":my_service_list,"assigned_user":assigned_user,"payment_details":payment_details}
	except Exception as e:
		return {"status":False,"message":e}
	
#getting the service purchase details
def get_service_payment_details(service_payment_id):
	service_payment_details = []
	get_service_payment = frappe.db.get_all("Service Payment",{"name":service_payment_id},['name','payment_id','service_booked_date','amount'],order_by='idx ASC')
	for payment in get_service_payment:
		service_payment_details = {
			"id":payment.name,
			"payment_id":payment.payment_id,
			"payment_date":format_date(payment.service_booked_date),
			"amount_paid":payment.amount,
		}
	return service_payment_details