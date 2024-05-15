import frappe
from startinsights.custom import get_domain_name
from frappe.utils import now, getdate, today, format_date,format_time
from datetime import datetime


#get the events for both live and recorded events
@frappe.whitelist()
def get_events(user_id):
    status = False
    live_event_image_url = ""
    recorded_event_image_url = ""
    is_registered = False
    try:
        events = frappe.db.get_all("SI Events",{"disabled":0},['*'],order_by='idx ASC')
        live_event_list = []
        recorded_event_list = []
        for event in events:
            if event.type_of_event == "Live Event":
                if event.live_event_image:
                    live_event_image_url = get_domain_name() + event.live_event_image
                else:
                    live_event_image_url = ""    
                start_time_change = change_time_format(format_time(event.event_start_date_time))
                end_time_change = change_time_format(format_time(event.event_end_date_time))
                if frappe.db.exists("Registered Event",{"user_id":user_id,"event_id":event.name}):
                    is_registered = True
                else:
                    is_registered = False    
                speakers_table = frappe.db.get_all("Event Speakers Table",{"parent":event.name},['speakers_name',"description"],order_by='idx ASC')
                live_event = {
                    "id":event.name,
                    "event_id":event.name,
                    "event_image":live_event_image_url,
                    "title":event.live_event_title,
                    "event_start_date":format_date(event.event_start_date_time),
                    "event_end_date":format_date(event.event_end_date_time),
                    "event_start_time":start_time_change,
                    "event_end_time":end_time_change,
                    "is_registered":is_registered,
                    "description":event.live_event_description,
                    "event_speakers":speakers_table,
                    "register_link":event.register
                }
                live_event_list.append(live_event)
                status = True
            if event.type_of_event == "Recorded Event":
                if event.record_event_image:
                    recorded_event_image_url = get_domain_name() + event.record_event_image
                else:
                    recorded_event_image_url = "" 
                recorded_event = {
                    "id":event.name,
                    "event_id":event.name,
                    "event_image":recorded_event_image_url,
                    "title":event.record_event_title,
                    "event_url":event.youtube_link or "",
                    "description":event.recorded_description
                }
                recorded_event_list.append(recorded_event)
                status = True
        return {"status":status,"live_event":live_event_list,"recorded_event":recorded_event_list}        
    except Exception as e:
        return {"status":False,"message":e}

#user registered events
@frappe.whitelist()
def create_registered_event(user_id,event_id):
    status = ""
    message = ""
    try:
        if not frappe.db.exists("Registered Event",{"user_id":user_id,"event_id":event_id}):
            new_event_register = frappe.new_doc("Registered Event")
            new_event_register.user_id = user_id
            new_event_register.event_id = event_id
            new_event_register.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("Pitch Room",new_event_register.name,'owner',user_id)
            status = True
            message = "Event Registered"
        else:
            status = False
            message = "Already Event Registered" 
        return {"status":status,"message":message}    
    except Exception as e:
        return {"status":False,"message":e}

#pass the time and get the session of AM or PM
def check_am_pm(session_time):
    try:
        # Parse the time string
        time_obj = datetime.strptime(session_time, "%H:%M")
        # Check if the hour is less than 12, if yes, it's AM, otherwise PM
        if time_obj.hour < 12:
            return "AM"
        else:
            return "PM"
    except ValueError:
        return "Invalid time format"

def change_time_format(time_change):
    time_obj = datetime.strptime(time_change, "%H:%M")    
    time_12hr = time_obj.strftime("%I:%M %p")
    return time_12hr