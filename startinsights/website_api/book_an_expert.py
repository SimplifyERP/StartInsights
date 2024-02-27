import frappe
import html2text
from frappe.utils import add_days,getdate,date_diff,now_datetime, add_to_date,formatdate,get_time, get_first_day,today,format_time,get_datetime
from frappe.utils import  get_url
from startinsights.custom import get_domain_name
from datetime import datetime, timedelta

@frappe.whitelist()
def book_an_expert(expert_id):
    expert_list = []
    description = ""
    image_url = ""
    booking_status = ""
    try:
        get_book_an_expert = frappe.db.get_all("Book an Expert",{'docstatus':1,'name':expert_id},['*'])
        formatted_book_an_expert = []
        current_time = datetime.now().time()
        time_since_midnight = timedelta(
        hours=current_time.hour,
        minutes=current_time.minute,
        seconds=current_time.second,
        microseconds=current_time.microsecond
)
 
        for expert in get_book_an_expert:
            description = html2text.html2text(expert.description).strip()
            if expert.attach_image:
                image_url = get_domain_name() + expert.attach_image
            else:
                image_url = ""    
            expert_list = {
                "expert_name":expert.full_name,
                "designation":expert.designation,
                "price":expert.pricing,
                "attach_image":image_url,
                "description":description,
                "from_date":formatdate(expert.from_date),
                "to_date":formatdate(expert.to_date),
                "start_time":expert.start_time,
                "end_time":expert.end_time,
                "duration":expert.duration,
                "booking":[]
            }
            booking = frappe.db.get_all('Book an Expert Table',{'parent': expert.name},['date','start_time','end_time','status'],order_by='idx ASC')
            expert['booking'] = []

            for book in booking:
                if book.date >= datetime.now().date(): 
                    book_time = book.start_time - timedelta(minutes=15)
                    if not time_since_midnight >= book_time: 
                        if book.status == "True":
                            booking_status = bool(True)
                        else:
                            booking_status = bool(False)    
                        expert_list['booking'].append({
                            "date":formatdate(book.date),
                            "start_time":book.start_time,
                            "end_time":book.end_time,
                            "status":booking_status,
                            "current_time":time_since_midnight
                        })
            formatted_book_an_expert.append(expert_list)    
        return {"status":True,"book_an_expert":formatted_book_an_expert, "current_time":time_since_midnight,"book_time":expert.start_time}
    except Exception as e:
        return {"status":False,"message":str(e)}


@frappe.whitelist()
def get_book_an_expert_list():
    description = ""
    image_url = ""
    try:
        get_book_an_expert = frappe.db.get_all("Book an Expert",{'docstatus':1},['*'],order_by='idx ASC')
        formatted_book_an_expert = []
        for expert in get_book_an_expert:
            description = html2text.html2text(expert.short_description).strip()
            if expert.attach_image:
                image_url = get_domain_name() + expert.attach_image
            else:
                image_url = ""    
            expert_list = {
                "id":expert.name,
                "expert_name":expert.full_name,
                "designation":expert.designation,
                "attach_image":image_url,
                "price":expert.pricing,
                "description":description,
            }
            formatted_book_an_expert.append(expert_list)    
        return {"status":True,"book_an_expert_list":formatted_book_an_expert}
    except Exception as e:
        return {"status":False,"message":e}
