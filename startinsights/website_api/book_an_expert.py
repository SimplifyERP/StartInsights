import frappe
import html2text
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate,get_time, get_first_day
from frappe.utils import  get_url
from startinsights.custom import get_domain_name
@frappe.whitelist()
def book_an_expert(expert_id):
    expert_list = []
    description = ""
    image_url = ""
    booking_status = ""
    try:
        get_book_an_expert = frappe.db.get_all("Book an Expert",{'docstatus':1,'name':expert_id},['*'])
        formatted_book_an_expert = []
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
                #added new condition for bool type
                if book.status == "True":
                    booking_status = bool(True)
                else:
                    booking_status = bool(False)    
                expert_list['booking'].append({
                    "date":formatdate(book.date),
                    "start_time":book.start_time,
                    "end_time":book.end_time,
                    "status":booking_status
                })
            formatted_book_an_expert.append(expert_list)    
        return {"status":True,"book_an_expert":formatted_book_an_expert}
    except Exception as e:
        return {"status":False,"message":e}
    

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
