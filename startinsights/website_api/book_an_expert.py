import frappe
import html2text
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate,get_time, get_first_day
from frappe.utils import  get_url

@frappe.whitelist()
def book_an_expert(expert_id):
    expert_list = []
    description = ""
    image_url = ""
    try:
        get_book_an_expert = frappe.db.get_all("Book an Expert",{'docstatus':1,'name':expert_id},['*'])
        formatted_book_an_expert = []
        for expert in get_book_an_expert:
            description = html2text.html2text(expert.description).strip()
            if expert.attach_image:
                image_url = get_url() + expert.attach_image
            else:
                image_url = ""    
            expert_list = {
                "expert_name":expert.full_name,
                "designation":expert.designation,
                "linkedin_id":expert.linkedin or "",
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
            booking = frappe.db.get_all('Book an Expert Table',{'parent': expert.name,'booked_status':0},['date','start_time','end_time'],order_by='idx ASC')
            expert['booking'] = []

            for book in booking:
                expert_list['booking'].append({
                    "date":formatdate(book.date),
                    "start_time":book.start_time,
                    "end_time":book.end_time,
                })
            formatted_book_an_expert.append(expert_list)    
        return {"status":True,"book_an_expert":formatted_book_an_expert}
    except Exception as e:
        return {"status":False,"message":e}
    

@frappe.whitelist()
def get_book_an_expert_list():
    expert_list = []
    description = ""
    image_url = ""
    try:
        get_book_an_expert = frappe.db.get_all("Book an Expert",{'docstatus':1},['*'])
        formatted_book_an_expert = []
        for expert in get_book_an_expert:
            description = html2text.html2text(expert.short_description).strip()
            if expert.attach_image:
                image_url = get_url() + expert.attach_image
            else:
                image_url = ""    
            expert_list = {
                "id":expert.name,
                "expert_name":expert.full_name,
                "designation":expert.designation,
                "linkedin_id":expert.linkedin,
                "attach_image":image_url,
                "price":expert.pricing,
                "description":description,
            }
            formatted_book_an_expert.append(expert_list)    
            return {"status":True,"book_an_expert_list":formatted_book_an_expert}
    except Exception as e:
        return {"status":False,"message":e}
