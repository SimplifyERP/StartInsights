import frappe
import html2text
from frappe.utils import add_days,getdate,date_diff,now_datetime, add_to_date,formatdate,get_time, get_first_day,today,format_time,get_datetime
from startinsights.custom import get_domain_name
from datetime import datetime, timedelta

@frappe.whitelist()
def expert_details(expert_id):
    # expert_list = []
    description = ""
    expert_description = ""
    # image_url = ""
    # booking_status = ""
    try:
        fundraising_experts = frappe.db.get_all("Fundraising Experts",{'disabled':0},['*'],order_by='idx ASC')
        fundraising_list = []
        for expert in fundraising_experts:
            current_time = datetime.now().time()
            time_since_midnight = timedelta(
            hours=current_time.hour,
            minutes=current_time.minute,
            seconds=current_time.second,
            microseconds=current_time.microsecond
            )
            if expert.short_description:
                description = html2text.html2text(expert.short_description).strip()
            else:
                description = ""    
            if expert.description:
                expert_description = expert.description
            else:
                expert_description = "" 
            if expert.expert_image:
                image_url = get_domain_name() + expert.expert_image
            else:
                image_url = ""      
            expert_list = {
                "id":expert.name,
                "name":expert.name,
                "expert_name":expert.full_name,
                "attach_image":image_url,
                "designation":expert.designation or "",
                "mail_id":expert.expert_mail_id or "",
                "price":frappe.utils.fmt_money(expert.pricing),
                "short_description":description,
                "description":expert_description,
                "from_date":formatdate(expert.from_date),
                "to_date":formatdate(expert.to_date),
                "start_time":expert.start_time,
                "end_time":expert.end_time,
                "duration":expert.duration,
                "booking":[]
            }
            expert_booking = frappe.db.get_all("Fundraising Expert Table",{'parent': expert.name},['date','start_time','end_time','status'],order_by='idx ASC')
            expert['booking'] = []
            for book in expert_booking:
                if book.date >= datetime.now().date(): 
                    book_time = book.start_time - timedelta(minutes=15)
                    if not time_since_midnight >= book_time: 
                        if book.status == "True":
                            booking_status = bool(True)
                        else:
                            booking_status = bool(False)    
                        expert_list['booking'].append({
                            "date":formatdate(book.date),
                            "start_time":format_time(book.start_time),
                            "end_time":format_time(book.end_time),
                            "status":booking_status,
                            "current_time":time_since_midnight
                        })
            fundraising_list.append(expert_list)    
        return {"status":True,"book_an_expert":fundraising_list, "current_time":format_time(time_since_midnight),"book_time":format_time(expert.start_time)}
    except Exception as e:
        return {"status":False,"message":str(e)}


@frappe.whitelist()
def get_fundraising_experts():
    image_url = ""
    description = ""
    expert_description = ""
    try:
        fundraising_experts = frappe.db.get_all("Fundraising Experts",{'disabled':0},['*'],order_by='idx ASC')
        fundraising_list = []
        for expert in fundraising_experts:
            if expert.short_description:
                description = html2text.html2text(expert.short_description).strip()
            else:
                description = ""    
            if expert.description:
                expert_description = expert.description
            else:
                expert_description = ""     
            if expert.expert_image:
                image_url = get_domain_name() + expert.expert_image
            else:
                image_url = ""    
            expert_list = {
                "id":expert.name,
                "name":expert.name,
                "expert_name":expert.full_name,
                "attach_image":image_url,
                "designation":expert.designation or "",
                "mail_id":expert.expert_mail_id or "",
                "price":frappe.utils.fmt_money(expert.pricing),
                "short_description":description,
                "description":expert_description
            }
            fundraising_list.append(expert_list)    
        return {"status":True,"fundraising_experts":fundraising_list}
    except Exception as e:
        return {"status":False,"message":e}
