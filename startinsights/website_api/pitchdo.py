import frappe
import html2text
from frappe.utils import  get_url
from startinsights.custom import get_domain_name



@frappe.whitelist()
def get_pitchdo():
    description = ""
    image_url = ""
    try:
        pitchdo = frappe.db.get_all("Pitch Do",['*'])
        formatted_pitch_do = [] 
        for pitch in pitchdo:
            description = html2text.html2text(pitch.short_description).strip()
            if pitch.pitch_image:
                image_url = get_domain_name() + pitch.pitch_image
            else:
                image_url = ""    
            pitch_do_details = {
                "id":pitch.name,
                "pitch_do_name":pitch.pitchdo_title_name,
                "pitch_image":image_url,
                "description":description
            }
            formatted_pitch_do.append(pitch_do_details)
        return {"status":True,"pitch_do":formatted_pitch_do}    
    except Exception as e:
        return {"status":False,"message":e}