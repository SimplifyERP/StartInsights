import frappe
from frappe.utils import now, getdate, today, format_date
from datetime import datetime
import html2text
from frappe.utils import  get_url


# pitch craft service details view
@frappe.whitelist()
def pitch_craft_list():
    image_url = ""
    plain_text_short_description = ""
    try:
        pitch_craft_list = frappe.db.get_all('Pitch Craft',{'pitch_craft_status':"Unsaved"},['name','service_name','pricing','short_description','pitch_craft_image'],order_by='idx ASC')
        formatted_pitch_craft_list = []
        for pitch_craft in pitch_craft_list:
            plain_text_short_description = html2text.html2text(pitch_craft.short_description).strip()
            if pitch_craft.pitch_craft_image:
                image_url = get_url() + pitch_craft.pitch_craft_image
            else:
                image_url = ""    
            pitch_craft_details = {
                'id': pitch_craft.name,
                'service_name': pitch_craft.service_name,
                "pitch_craft_image":image_url,
                'pricing': pitch_craft.pricing,
                'short_description': plain_text_short_description,
            }
            formatted_pitch_craft_list.append(pitch_craft_details)
        my_services = get_my_services_pitch_craft()    
        return {"status": True, "services_list": formatted_pitch_craft_list,"my_services":my_services}
    except Exception as e:
        return {"status": False, "message": str(e)}


def get_my_services_pitch_craft():
    image_url = ""
    plain_text_short_description = ""
    try:
        pitch_craft_list = frappe.db.get_all('Pitch Craft',{'pitch_craft_status':"Saved"},['name','service_name','pricing','short_description','pitch_craft_image'],order_by='idx ASC')
        formatted_pitch_craft_list = []
        for pitch_craft in pitch_craft_list:
            plain_text_short_description = html2text.html2text(pitch_craft.short_description).strip()
            if pitch_craft.pitch_craft_image:
                image_url = get_url() + pitch_craft.pitch_craft_image
            else:
                image_url = ""    
            pitch_craft_details = {
                'id': pitch_craft.name,
                'service_name': pitch_craft.service_name,
                "pitch_craft_image":image_url,
                'pricing': pitch_craft.pricing,
                'short_description': plain_text_short_description,
            }
            formatted_pitch_craft_list.append(pitch_craft_details)
        return formatted_pitch_craft_list
    except Exception as e:
        return {"message": str(e)}  
    

# pitch craft overview details
@frappe.whitelist()
def pitch_craft_overview_details(name):
    plain_text_short_description = ""
    plain_text_benefits = ""
    image_url = ""
    try:
        pitch_craft = frappe.get_doc('Pitch Craft', name)
        if not pitch_craft:
            return {"status": False, "message": f"Pitch Craft '{name}' not found"}
        plain_text_short_description = html2text.html2text(pitch_craft.description).strip()
        plain_text_benefits = html2text.html2text(pitch_craft.benefits).strip()
        if pitch_craft.pitch_craft_image:
            image_url = get_url() + pitch_craft.pitch_craft_image
        else:
            image_url = ""    
        formatted_pitch_craft_details = {
            'id': pitch_craft.name,
            'service_name': pitch_craft.service_name,
            "pitch_craft_image":image_url,
            'pricing': pitch_craft.pricing,
            'benefits': plain_text_benefits,
            'description': plain_text_short_description,
        }
        return {"status": True, "pitch_craft_overview_details": formatted_pitch_craft_details}
    except:
        return {"status": False}

# pitch craft process & document details
@frappe.whitelist()
def pitch_craft_process_details(name):
    plain_text_deliverables = ""
    image_url = ""
    try:
        pitch_craft = frappe.get_doc('Pitch Craft', name)
        pitch_craft_list = []
        if not pitch_craft:
            return {"status": False, "message": f"Pitch Craft '{name}' not found"}
        plain_text_deliverables = html2text.html2text(pitch_craft.deliverables).strip()
        if pitch_craft.pitch_craft_image:
            image_url = get_url() + pitch_craft.pitch_craft_image
        else:
            image_url = "" 
        pitch_craft_details = {
            'id': pitch_craft.name,
            'service_name': pitch_craft.service_name,
            "pitch_craft_image":image_url,
            'pricing': pitch_craft.pricing,
            'deliverables': plain_text_deliverables,
            'documents_required':[],
        }
        documents_required = frappe.db.get_all("Pitch Craft Documents Table",{'parent':name},['documents_required'],order_by='idx ASC')
        for documents in documents_required:
            pitch_craft_details['documents_required'].append({
                "documents":documents.documents_required
            })
        pitch_craft_list.append(pitch_craft_details)    
        return {"status": True, "pitch_craft_process_details": pitch_craft_list}
    except:
        return {"status": False}

# pitch craft full details
@frappe.whitelist()
def pitch_craft_service_details(name):
    plain_text_short_description = ""
    plain_text_benefits = ""
    plain_text_deliverables = ""
    image_url = ""
    try:
        pitch_craft = frappe.get_doc('Pitch Craft', name)
        pitch_craft_list = []
        if not pitch_craft:
            return {"status": False, "message": f"Pitch Craft '{name}' not found"}
        plain_text_short_description = html2text.html2text(pitch_craft.description).strip()
        plain_text_benefits = html2text.html2text(pitch_craft.benefits).strip()
        plain_text_deliverables = html2text.html2text(pitch_craft.deliverables).strip()
        if pitch_craft.pitch_craft_image:
            image_url = get_url()+ pitch_craft.pitch_craft_image
        else:
            image_url = ""    
        pitch_craft_details = {
            'id': pitch_craft.name,
            'service_name': pitch_craft.service_name,
            "pitch_craft_image":image_url,
            'pricing': pitch_craft.pricing,
            'benefits': plain_text_benefits,
            'description': plain_text_short_description,
            'deliverables': plain_text_deliverables,
            'documents_required':[],
        }
        documents_required = frappe.db.get_all("Pitch Craft Documents Table",{'parent':name},['documents_required'],order_by='idx ASC')
        for documents in documents_required:
            pitch_craft_details['documents_required'].append({
                "documents":documents.documents_required
            })
        pitch_craft_list.append(pitch_craft_details)    
        return {"status": True, "pitch_craft_service_details": pitch_craft_list}
    except:
        return {"status": False}



#get the saved and unsaved courses list
@frappe.whitelist()
def get_saved_pitch_craft(pitch_id,status):
    message = ""
    try:
        if status:
            frappe.db.set_value("Pitch Craft",pitch_id,'pitch_craft_status',status)
            message = "%s course update as %s"%(pitch_id,status)
            return {"status": True, "message":message} 
        else:
            message = "Please Put the Status"
            return {"status": False, "message":message} 
    except Exception as e:
        return {"status": False, "message": str(e)}
    