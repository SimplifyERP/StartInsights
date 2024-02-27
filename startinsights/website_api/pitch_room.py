import frappe
from frappe.utils import get_url
import html2text
import base64
from frappe.utils.file_manager import save_file
from datetime import datetime
from frappe.utils import now, getdate, today, format_date
from startinsights.custom import get_domain_name


# Creating a new pitch room list
@frappe.whitelist()
def create_pitch_room(room_name, description,pitch_deck,projections,executive_summary,pitch_deck_doc_type,
                    projection_doc_type,executive_summary_doc_type,shared_user,expiry_date):
    try:
        expiry_date_format = datetime.strptime(str(expiry_date), "%d-%m-%Y").date()
        decoded_data_inside_1 = base64.b64decode(pitch_deck)
        decoded_data_inside_2 = base64.b64decode(projections)
        decoded_data_inside_3 = base64.b64decode(executive_summary)
        #creating a new pitch room through api
        new_room = frappe.new_doc('Pitch Room')
        new_room.room_name = room_name
        new_room.description = description
        new_room.shared_user = shared_user
        new_room.pitch_deck_doc_type = pitch_deck_doc_type
        new_room.projection_doc_type = projection_doc_type
        new_room.executive_summary_doc_type = executive_summary_doc_type
        new_room.expiry_date = expiry_date_format
        new_room.save(ignore_permissions=True)
        frappe.db.commit()
        # the below method the giving the pitch deck attach in file list
        if pitch_deck:
            attach_pitch_deck(new_room,pitch_deck_doc_type,decoded_data_inside_1)
        #the below method the giving the projections attach in file list
        if projections:
            attach_projections(new_room,projection_doc_type,decoded_data_inside_2)
        #the below method the giving the executive_summary attach in file list
        if executive_summary:
            attach_executive_summary(new_room,executive_summary_doc_type,decoded_data_inside_3)
        return {'status':True,"message":"New Pitch Room Created"}
    except Exception as e:
        status = False
        return {'status': status, 'message': str(e)}

def attach_pitch_deck(new_room,pitch_deck_doc_type,decoded_data_inside_1):
    if pitch_deck_doc_type == "pdf":
        file_name_inside = f"{new_room.name.replace(' ', '_')}document.pdf"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = decoded_data_inside_1
        new_file_inside.attached_to_doctype = "Pitch Room"
        new_file_inside.attached_to_name = new_room.name
        new_file_inside.attached_to_field = "pitch_deck"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("Pitch Room",new_room.name,'pitch_deck',new_file_inside.file_url)
    elif pitch_deck_doc_type == "xlsx":
        file_name_inside = f"{new_room.name.replace(' ', '_')}document.xlsx"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = decoded_data_inside_1
        new_file_inside.attached_to_doctype = "Pitch Room"
        new_file_inside.attached_to_name = new_room.name
        new_file_inside.attached_to_field = "pitch_deck"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("Pitch Room",new_room.name,'pitch_deck',new_file_inside.file_url)
    elif pitch_deck_doc_type == "docx":
        file_name_inside = f"{new_room.name.replace(' ', '_')}document.docx"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = decoded_data_inside_1
        new_file_inside.attached_to_doctype = "Pitch Room"
        new_file_inside.attached_to_name = new_room.name
        new_file_inside.attached_to_field = "pitch_deck"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("Pitch Room",new_room.name,'pitch_deck',new_file_inside.file_url)    
    else:
        return "The Given document is not a Image or PDF"    

def attach_projections(new_room,projection_doc_type,decoded_data_inside_2):
    if projection_doc_type == "pdf":
        file_name_inside = f"{new_room.name.replace(' ', '_')}document.pdf"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = decoded_data_inside_2
        new_file_inside.attached_to_doctype = "Pitch Room"
        new_file_inside.attached_to_name = new_room.name
        new_file_inside.attached_to_field = "projections"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("Pitch Room",new_room.name,'projections',new_file_inside.file_url)
    elif projection_doc_type == "xlsx":
        file_name_inside = f"{new_room.name.replace(' ', '_')}document.xlsx"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = decoded_data_inside_2
        new_file_inside.attached_to_doctype = "Pitch Room"
        new_file_inside.attached_to_name = new_room.name
        new_file_inside.attached_to_field = "projections"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("Pitch Room",new_room.name,'projections',new_file_inside.file_url)
    elif projection_doc_type == "docx":
        file_name_inside = f"{new_room.name.replace(' ', '_')}document.docx"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = decoded_data_inside_2
        new_file_inside.attached_to_doctype = "Pitch Room"
        new_file_inside.attached_to_name = new_room.name
        new_file_inside.attached_to_field = "projections"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("Pitch Room",new_room.name,'projections',new_file_inside.file_url)    
    else:
        return "The Given document is not a Image or PDF"
    
def attach_executive_summary(new_room,executive_summary_doc_type,decoded_data_inside_3):
    if executive_summary_doc_type == "pdf":
        file_name_inside = f"{new_room.name.replace(' ', '_')}document.pdf"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = decoded_data_inside_3
        new_file_inside.attached_to_doctype = "Pitch Room"
        new_file_inside.attached_to_name = new_room.name
        new_file_inside.attached_to_field = "executive_summary"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("Pitch Room",new_room.name,'executive_summary',new_file_inside.file_url)
    elif executive_summary_doc_type == "xlsx":
        file_name_inside = f"{new_room.name.replace(' ', '_')}document.xlsx"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = decoded_data_inside_3
        new_file_inside.attached_to_doctype = "Pitch Room"
        new_file_inside.attached_to_name = new_room.name
        new_file_inside.attached_to_field = "executive_summary"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("Pitch Room",new_room.name,'executive_summary',new_file_inside.file_url)
    elif executive_summary_doc_type == "docx":
        file_name_inside = f"{new_room.name.replace(' ', '_')}document.docx"
        new_file_inside = frappe.new_doc('File')
        new_file_inside.file_name = file_name_inside
        new_file_inside.content = decoded_data_inside_3
        new_file_inside.attached_to_doctype = "Pitch Room"
        new_file_inside.attached_to_name = new_room.name
        new_file_inside.attached_to_field = "executive_summary"
        new_file_inside.is_private = 0
        new_file_inside.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.db.set_value("Pitch Room",new_room.name,'executive_summary',new_file_inside.file_url)    
    else:
        return "The Given document is not a Image or PDF"    
        


# pitch room details view
@frappe.whitelist()
def pitch_room_list():
    doc_1 = ""
    doc_2 = ""
    doc_3 = ""
    try:
        pitch_room_list = frappe.db.get_all('Pitch Room', ['*'], order_by='idx ASC')
        formatted_pitch_room_list = []
        for pitch_room in pitch_room_list:
            doc_1 = get_domain_name() + pitch_room.pitch_deck if pitch_room.pitch_deck else ""
            doc_2 = get_domain_name() + pitch_room.projections if pitch_room.projections else ""
            doc_3 = get_domain_name() + pitch_room.executive_summary if pitch_room.executive_summary else ""

            pitch_room_details = {
                'id': pitch_room.name,
                'room_name': pitch_room.room_name,
                'description': pitch_room.description,
                'pitch_deck': doc_1,
                'projections': doc_2,
                'executive_summary': doc_3,
                'shared_user':pitch_room.shared_user,
                'expiry_date':format_date(pitch_room.expiry_date)
            }
            formatted_pitch_room_list.append(pitch_room_details)
        return {"status": True, "pitch_room_details": formatted_pitch_room_list}
    except Exception as e:
        frappe.log_error(f"Error in pitch_room_list: {str(e)}")
        return {"status": False}

# individual pitch room doc taken code
@frappe.whitelist()
def pitch_room(id):
    description = ""
    room_list = ""
    try:
        pitch_room= frappe.db.get_all("Pitch Room",{'name':id},['*'])
        formatted_pitch_room = []
        for room in pitch_room:
            description = html2text.html2text(room.description).strip()
            if room.pitch_deck:
                doc_1 = get_domain_name() + room.pitch_deck
            else:
                doc_1 = ""

            if room.projections:
                doc_2 = get_domain_name() + room.projections
            else:
                doc_2 = "" 

            if room.executive_summary:
                doc_3 = get_domain_name() + room.executive_summary
            else:
                doc_3 = ""  
            room_list = {
                "name":room.room_name,
                "room_name":room.room_name,
                "description":description or '',
                "pitch_deck":doc_1,
                "projections":doc_2,
                "executive_summary":doc_3, 
                "shared_user":pitch_room.shared_user,
                "expiry_date":format_date(pitch_room.expiry_date) 
            }
            formatted_pitch_room.append(room_list)
        return {"status":True,"pitch_room":formatted_pitch_room}
    except Exception as e:
        return {"status":False,"message":e}

@frappe.whitelist()
def get_users_with_role():
    user_type = "Investors"
    image_url = ""
    get_profile_details = frappe.db.get_all("Profile Application",{"type_of_user":user_type},['*'])
    format_user = []
    for profile in get_profile_details:
        if profile.profile_image:
            image_url = get_domain_name() + profile.profile_image
        else:
            image_url = ""    
        user_role = {
            "user_id":profile.user_id,
            "full_name":profile.full_name,
            "profile_image":image_url,
            "email_id":profile.email_id,
            "designation":profile.designation
        }
        format_user.append(user_role)
    return {"status":True,"user_role":format_user}
if __name__ == "__main__":
    students_users = get_users_with_role()
    print(f"Users with the role 'Students': {students_users}")
