import frappe
from frappe.utils import now, getdate, today, format_date,format_time
from datetime import datetime
import html2text
from startinsights.custom import get_domain_name
import json
from bs4 import BeautifulSoup
import base64
import locale



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
			formated_currency = "{:,.0f}".format(service.pricing)
			#added the domain name with image url
			if service.service_image:
				image_url = get_domain_name() + service.service_image
			else:
				image_url = ""    
			#response	
			service_details = {
				"id": service.name,
				"name":service.name,
				"service_name": service.service_name or "",
				"service_image":image_url,
				"pricing":int(service.pricing or 0),
				"pricing_format":formated_currency,
				"short_description": format_short_description or "",
				"about_service":format_about_service or "",
				"deliverables":format_deliverables or "",
				"documents":[],
				"process_steps":[],
				"status_doc_upload":[],
				"service_deliverables_doc":[],
				'purchase_status':purchase_status,
				"service_status":"",	
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
	doc_upload_status = False
	process_status = False
	doc_url = ""
	deliverable_url = ""
	try:
		my_services = frappe.db.get_all('My Services',{'user':user_id},['*'],order_by='idx ASC')
		service_payment_list = []
		for service in my_services:
			#by passing the service id to get all service details
			service_detail = frappe.get_doc("Services",service.service_id)
			#by getting the text editor data to remove the html tags
			format_short_description = html2text.html2text(service_detail.short_description or "").strip() 
			format_about_service = html2text.html2text(service_detail.about_service or "").strip() 
			format_deliverables = html2text.html2text(service_detail.deliverables or "").strip() 
			formated_currency = "{:,.0f}".format(service_detail.pricing)
			#by concedation the domain name and image url path to show image or anything
			if service_detail.service_image:
				image_url = get_domain_name() + service_detail.service_image
			else:
				image_url = ""    
			service_details = {
				"id": service.name,
				"name":service.name,
				"service_name": service_detail.service_name or "",
				"service_image":image_url,
				"pricing":service_detail.pricing or 0,
				"pricing_format":formated_currency,
				"short_description": format_short_description or "",
				"about_service":format_about_service or "",
				"deliverables":format_deliverables or "",
				"documents":[],
				"process_steps":[],
				"status_doc_upload":[],
				"service_deliverables_doc":[],
				'purchase_status':True,
				"service_status":service.service_status or "",
			}

			service_documents = frappe.db.get_all("Service Documents",{'parent':service.service_id},["*"],order_by='idx ASC')
			for documents in service_documents:
				service_details['documents'].append({
					"documents":documents.documents_required or ""
				})

			get_process_steps = frappe.db.get_all("Process Steps",{'parent':service.name},["*"],order_by='idx ASC')
			for process in get_process_steps:
				if process.status == "Completed":
					process_status = True
				else:
					process_status = False
				if process.doc_upload == 1:
					doc_upload_status = True
				else:
					doc_upload_status = False	
				service_details["process_steps"].append({
					"steps":process.steps or "",
					"tat":process.tat or "",
					"current_status":process.status or "",
					"step_status":process_status,
					"doc_status":doc_upload_status
				})

			get_doc_upload = frappe.db.get_all("Services Document Upload Table",{'parent':service.name},["*"],order_by='idx ASC')	
			for user_doc in get_doc_upload:
				if user_doc.doc_attach:
					doc_url = get_domain_name() + user_doc.doc_attach
				else:
					doc_url = ""	
				service_details["status_doc_upload"].append({
					"service_status":user_doc.service_status or "",
					"doc_extension":user_doc.doc_extension or "",
					"doc_name":user_doc.doc_name or "",
					"doc_url":doc_url,
				})

			get_deliverable_document = frappe.db.get_all("Services Document Upload Table",{'parent':service.name},["*"],order_by='idx ASC')	
			for deliverable in get_deliverable_document:
				if deliverable.documents_attach:
					deliverable_url = get_domain_name() +  deliverable.documents_attach
				else:
					deliverable_url = ""	
				service_details["service_deliverables_doc"].append({
					"document_name":deliverable.document_name or "",
					"doc_attach":deliverable_url
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
		new_service_payment.submit()
		frappe.db.commit()
		frappe.db.set_value("Service Payment",new_service_payment.name,'owner',user)

		create_my_services(user,service_id,new_service_payment.name)

		return {"status": True,"message":"Service Payment Created"}
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
def get_my_service_details(my_service_id,doctype,user_id):
	image_url = ""
	user_image = ""
	assigned_user = []
	chat_conversation = []
	payment_details = []
	process_status = False
	doc_upload_status = False
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
		formated_currency = "{:,.0f}".format(get_master_services.pricing)
		my_service_details = {
			"id": my_service.name,
			"name":my_service.name,
			"service_name": get_master_services.service_name or "",
			"service_image":image_url,
			"pricing":get_master_services.pricing or 0,
			"pricing_format": formated_currency,
			"short_description": format_short_description or "",
			"about_service":format_about_service or "",
			"deliverables":format_deliverables or "",
			"documents":[],
			"process_steps":[],
			"status_doc_upload":[],
			"service_deliverables_doc":[],
			'purchase_status':True,
			"service_status":my_service.service_status or "",
			
		}
		service_documents = frappe.db.get_all("Service Documents",{'parent':get_master_services.name},["*"],order_by='idx ASC')
		for documents in service_documents:
			my_service_details['documents'].append({
					"documents":documents.documents_required or ""
				})
		get_process_steps = frappe.db.get_all("Process Steps",{'parent':my_service.name},["*"],order_by='idx ASC')
		for process in get_process_steps:
			if process.status == "Completed":
				process_status = True
			else:
				process_status = False
			if process.doc_upload == 1:
				doc_upload_status = True
			else:
				doc_upload_status = False	
			my_service_details["process_steps"].append({
				"steps":process.steps or "",
				"tat":process.tat or "",
				"current_status":process.status or "",
				"step_status":process_status,
				"doc_status":doc_upload_status
			})

		get_doc_upload = frappe.db.get_all("Services Document Upload Table",{'parent':my_service.name},["*"],order_by='idx ASC')	
		for user_doc in get_doc_upload:
			if user_doc.doc_attach:
				doc_url = get_domain_name() + user_doc.doc_attach
			else:
				doc_url = ""	
			my_service_details["status_doc_upload"].append({
				"service_status":user_doc.service_status or "",
				"doc_extension":user_doc.doc_extension or "",
				"doc_name":user_doc.doc_name or "",
				"doc_url":doc_url,
			})

		get_deliverable_document = frappe.db.get_all("My Service Deliverables",{'parent':my_service.name},["*"],order_by='idx ASC')	
		for deliverable in get_deliverable_document:
			if deliverable.documents_attach:
				deliverable_url = get_domain_name() +  deliverable.documents_attach
			else:
				deliverable_url = ""	
			my_service_details["service_deliverables_doc"].append({
				"document_name":deliverable.document_name or "",
				"doc_attach":deliverable_url
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
		chat_conversation = get_chat_conversation(my_service,doctype,user_id)
		return {"status":True,"my_service_details":my_service_list,"assigned_user":assigned_user,"payment_details":payment_details,"chat_conversation":chat_conversation}
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

#user documents upload method
@frappe.whitelist()
def my_services_doc_upload(my_service_id,upload_doc):
	status = ""
	message = ""
	try:
		decode_json_users = json.loads(upload_doc)
		if not upload_doc == []:
			for upload in decode_json_users:
				document_type = upload.get("extension")
				doc_name = upload.get("name")
				attach = upload.get("attach")
				if document_type in ["pdf","docx","doc","xlsx","png","jpg","jpeg"]:
					file_name_inside = doc_name
					attach_converted_url = base64.b64decode(attach)
					new_file_inside = frappe.new_doc('File')
					new_file_inside.file_name = file_name_inside
					new_file_inside.content = attach_converted_url
					new_file_inside.attached_to_doctype = "Services Document Upload Table"
					new_file_inside.attached_to_name = my_service_id
					new_file_inside.attached_to_field = "attach" 
					new_file_inside.is_private = 0
					new_file_inside.save(ignore_permissions=True)
					frappe.db.commit()

					get_my_service = frappe.get_doc("My Services",my_service_id)
					get_my_service.append("status_documents_upload",{
						"service_status":upload.get("service_status"),
						"doc_extension":document_type,
						"doc_name":doc_name,
						"doc_attach":new_file_inside.file_url
					})
					get_my_service.save(ignore_permissions=True)
					frappe.db.commit()
					status = True
					message = "Success"
				else:
					status = False
					message = "The given document type is not supported"   
		else:
			status = False
			message = "Please attach the documents"			 	
		return {"status":status,"message":message}
	except Exception as e:
		return {"status":False,"message":e}
	


#get the all chat conversations against the user and service id
# @frappe.whitelist()
def get_chat_conversation(service_id,doctype,user_id):
	chat_boxes = []
	comments = frappe.db.get_all("Comment",filters={"reference_name":service_id,"reference_doctype":doctype,"comment_email":user_id},fields=['content','creation','custom_user'], order_by="creation ASC")
	if comments:
		# Extract comment content and format into chat box format
		chat_boxes = []
		for comment in comments:
			content = comment.get('content')
			custom_user = comment.get('custom_user')
			if content:
				# Remove HTML tags from the comment content
				comment_text = BeautifulSoup(content, "html.parser").get_text()
				# Convert creation timestamp to string
				creation_timestamp = str(comment.get('creation'))
				creation_date = format_date(creation_timestamp)
				creation_time = format_time(creation_timestamp)
				# Determine the position of the chat box based on custom_user checkbox
				place = "Right" if custom_user else "Left"
				chat_boxes.append({
					"chat_box": comment_text,
					"chat_date": creation_date,
					"chate_time": creation_time,
					"place": place
				})
		return chat_boxes
	else:
		return chat_boxes
