import frappe
from datetime import datetime
from frappe.utils import now,getdate,today,format_date,nowdate,add_months,get_time


@frappe.whitelist()
def create_service_list(expert_name,service_date,start_time,end_time,user,booking_id):
    status = ""
    message = ""
    try:
        service_date_format = datetime.strptime(format_date(service_date), "%m-%d-%Y").date()
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
        new_service.save(ignore_permissions=True)
        frappe.db.commit()

        mark_booked_status(booking_id,start_time,end_time,service_date)
        status = True
        message = "Service List Created"
        return {"status":status,"message":message}
    except Exception as e:
        status = False
        message = e
        return {"status":status,"message":message}
    
# mark the booked status in child table
def mark_booked_status(booking_id,start_time,end_time,date):
    service_date_format = datetime.strptime(format_date(date), "%m-%d-%Y").date()
    get_book_an_expert = frappe.get_doc("Book an Expert", booking_id)
    get_booking_table = frappe.db.get_all("Book an Expert Table",filters={'parent': get_book_an_expert.name},fields=['*'],order_by='idx ASC')
    for entry in get_booking_table:
        if entry.date == service_date_format:
            if get_time(entry.start_time) == get_time(start_time) and get_time(entry.end_time) == get_time(end_time):
                frappe.db.set_value("Book an Expert Table",entry.name,'booked_status','1')
       