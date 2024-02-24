import frappe
from datetime import datetime
from frappe.utils import now,getdate,today,format_date,nowdate,add_months,get_time

@frappe.whitelist()
def create_service_list(expert_name,service_date,start_time,end_time,user,booking_id,payment_id,amount,payment_method):
    status = ""
    message = ""
    try:
        service_date_format = datetime.strptime(str(service_date), "%d-%m-%Y").date()
        start_time_format = datetime.strptime(start_time, '%H:%M')
        end_time_format = datetime.strptime(end_time, '%H:%M')

        new_service = frappe.new_doc("Service Listing")
        new_service.expert_name = expert_name
        new_service.service_date = service_date_format
        new_service.start_time = start_time_format
        new_service.end_time = end_time_format
        new_service.user = user
        new_service.book_an_expert = booking_id
        new_service.status = "Paid"
        new_service.payment_id = payment_id
        new_service.service_amount = amount
        new_service.save(ignore_permissions=True)
        # new_service.payment_method = payment_method
        new_service.submit()
        frappe.db.commit()

        mark_booked_status(booking_id,start_time,end_time,service_date_format)
        status = True
        message = "Service List Created"
        return {"status":status,"message":message}
    except Exception as e:
        status = False
        message = e
        return {"status":status,"message":message}
    
# mark the booked status in child table
def mark_booked_status(booking_id,start_time,end_time,date):
    get_book_an_expert = frappe.get_doc("Book an Expert", booking_id)
    get_booking_table = frappe.db.get_all("Book an Expert Table",filters={'parent': get_book_an_expert.name},fields=['*'],order_by='idx ASC')
    for entry in get_booking_table:
        if entry.date == date:
            if get_time(entry.start_time) == get_time(start_time) and get_time(entry.end_time) == get_time(end_time):
                frappe.db.set_value("Book an Expert Table",entry.name,'booked_status','1')
                frappe.db.set_value("Book an Expert Table",entry.name,'status','True')


@frappe.whitelist()
def get_service_list_payment_details(user_id,booking_id):
    try:
        get_payment_details = frappe.db.get_all("Service Listing",{'user':user_id,'book_an_expert':booking_id},['payment_id','service_date','service_amount','start_time','end_time'],order_by='idx ASC')
        format_payment = []
        for payment in get_payment_details:
            service_payment_details = {
                "payment_id":payment.payment_id,
                "payment_date":format_date(payment.service_date),
                "amount_paid":payment.service_amount,
                "service_start_time":payment.start_time,
                "service_end_time":payment.end_time,
                # "payment_method":payment.payment_method or ""
            }
            format_payment.append(service_payment_details)
        return {"status":True,"service_list_payment_details":format_payment}    
    except Exception as e:
        return {"status":False,"message":e}