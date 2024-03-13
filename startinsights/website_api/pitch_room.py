import frappe
from frappe.utils import get_url
import html2text
import base64
from frappe.utils.file_manager import save_file
from datetime import datetime
from frappe.utils import now, getdate, today, format_date
from startinsights.custom import get_domain_name
from frappe import _, get_doc


# Creating a new pitch room list
@frappe.whitelist()
def create_pitch_room(cover_image,pitch_room_name,about_startup,user_id):
    status = ""
    message = ""
    try:
        cover_image_converted_image = base64.b64decode(cover_image)
        #creating a new pitch room through api
        if not frappe.db.exists("Pitch Room",{'room_name':pitch_room_name,'user_id':user_id}):
            new_room = frappe.new_doc('Pitch Room')
            new_room.room_name = pitch_room_name
            new_room.about_startup = about_startup
            new_room.user_id = user_id
            new_room.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("Pitch Room",new_room.name,'owner',user_id)

            file_name_inside = f"{new_room.name.replace(' ', '_')}cover_imgae.jpg"
            new_file_inside = frappe.new_doc('File')
            new_file_inside.file_name = file_name_inside
            new_file_inside.content = cover_image_converted_image
            new_file_inside.attached_to_doctype = "Pitch Room"
            new_file_inside.attached_to_name = new_room.name
            new_file_inside.attached_to_field = "cover_image"
            new_file_inside.is_private = 0
            new_file_inside.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("Pitch Room",new_room.name,'cover_image',new_file_inside.file_url)
            status = True
            message = "New Pitch Room Created"
        else:
            status = False
            message = "Pitch Room Name Same Please Create New Room Name"    
        return {'status':status,"message":message}
    except Exception as e:
        status = False
        return {'status': status, 'message': str(e)}

# pitch room details view
@frappe.whitelist()
def pitch_room_list(user_id):
    image_url = ""
    company_name = ""
    try:
        get_pitch_room = frappe.db.get_all('Pitch Room',{'user_id':user_id},['name','room_name','cover_image','about_startup'], order_by='idx ASC')
        get_pitch_room_list = []
        for pitch_room in get_pitch_room:
            get_company_name = frappe.db.get_value("Profile Application",{'user_id':user_id},['company_name'])
            if get_company_name:
                company_name = get_company_name
            else:
                company_name = ""    
            if pitch_room.cover_image:
                image_url = get_domain_name() + pitch_room.cover_image
            else:
                image_url = ""    
            pitch_room_details = {
                'id': pitch_room.name,
                "cover_image":image_url,
                'room_name': pitch_room.room_name,
                'company_name':company_name,
                'about_startup': pitch_room.about_startup,
            }
            get_pitch_room_list.append(pitch_room_details)
        return {"status": True, "pitch_room_details":get_pitch_room_list}
    except Exception as e:
        return {"status": False,"message":e}









# def attach_pitch_deck(new_room,pitch_deck_doc_type,decoded_data_inside_1):
#     if pitch_deck_doc_type == "pdf":
#         file_name_inside = f"{new_room.name.replace(' ', '_')}document.pdf"
#         new_file_inside = frappe.new_doc('File')
#         new_file_inside.file_name = file_name_inside
#         new_file_inside.content = decoded_data_inside_1
#         new_file_inside.attached_to_doctype = "Pitch Room"
#         new_file_inside.attached_to_name = new_room.name
#         new_file_inside.attached_to_field = "pitch_deck"
#         new_file_inside.is_private = 0
#         new_file_inside.save(ignore_permissions=True)
#         frappe.db.commit()
#         frappe.db.set_value("Pitch Room",new_room.name,'pitch_deck',new_file_inside.file_url)
#     elif pitch_deck_doc_type == "xlsx":
#         file_name_inside = f"{new_room.name.replace(' ', '_')}document.xlsx"
#         new_file_inside = frappe.new_doc('File')
#         new_file_inside.file_name = file_name_inside
#         new_file_inside.content = decoded_data_inside_1
#         new_file_inside.attached_to_doctype = "Pitch Room"
#         new_file_inside.attached_to_name = new_room.name
#         new_file_inside.attached_to_field = "pitch_deck"
#         new_file_inside.is_private = 0
#         new_file_inside.save(ignore_permissions=True)
#         frappe.db.commit()
#         frappe.db.set_value("Pitch Room",new_room.name,'pitch_deck',new_file_inside.file_url)
#     elif pitch_deck_doc_type == "docx":
#         file_name_inside = f"{new_room.name.replace(' ', '_')}document.docx"
#         new_file_inside = frappe.new_doc('File')
#         new_file_inside.file_name = file_name_inside
#         new_file_inside.content = decoded_data_inside_1
#         new_file_inside.attached_to_doctype = "Pitch Room"
#         new_file_inside.attached_to_name = new_room.name
#         new_file_inside.attached_to_field = "pitch_deck"
#         new_file_inside.is_private = 0
#         new_file_inside.save(ignore_permissions=True)
#         frappe.db.commit()
#         frappe.db.set_value("Pitch Room",new_room.name,'pitch_deck',new_file_inside.file_url)    
#     else:
#         return "The Given document is not a Image or PDF"    

# def attach_projections(new_room,projection_doc_type,decoded_data_inside_2):
#     if projection_doc_type == "pdf":
#         file_name_inside = f"{new_room.name.replace(' ', '_')}document.pdf"
#         new_file_inside = frappe.new_doc('File')
#         new_file_inside.file_name = file_name_inside
#         new_file_inside.content = decoded_data_inside_2
#         new_file_inside.attached_to_doctype = "Pitch Room"
#         new_file_inside.attached_to_name = new_room.name
#         new_file_inside.attached_to_field = "projections"
#         new_file_inside.is_private = 0
#         new_file_inside.save(ignore_permissions=True)
#         frappe.db.commit()
#         frappe.db.set_value("Pitch Room",new_room.name,'projections',new_file_inside.file_url)
#     elif projection_doc_type == "xlsx":
#         file_name_inside = f"{new_room.name.replace(' ', '_')}document.xlsx"
#         new_file_inside = frappe.new_doc('File')
#         new_file_inside.file_name = file_name_inside
#         new_file_inside.content = decoded_data_inside_2
#         new_file_inside.attached_to_doctype = "Pitch Room"
#         new_file_inside.attached_to_name = new_room.name
#         new_file_inside.attached_to_field = "projections"
#         new_file_inside.is_private = 0
#         new_file_inside.save(ignore_permissions=True)
#         frappe.db.commit()
#         frappe.db.set_value("Pitch Room",new_room.name,'projections',new_file_inside.file_url)
#     elif projection_doc_type == "docx":
#         file_name_inside = f"{new_room.name.replace(' ', '_')}document.docx"
#         new_file_inside = frappe.new_doc('File')
#         new_file_inside.file_name = file_name_inside
#         new_file_inside.content = decoded_data_inside_2
#         new_file_inside.attached_to_doctype = "Pitch Room"
#         new_file_inside.attached_to_name = new_room.name
#         new_file_inside.attached_to_field = "projections"
#         new_file_inside.is_private = 0
#         new_file_inside.save(ignore_permissions=True)
#         frappe.db.commit()
#         frappe.db.set_value("Pitch Room",new_room.name,'projections',new_file_inside.file_url)    
#     else:
#         return "The Given document is not a Image or PDF"
    
# def attach_executive_summary(new_room,executive_summary_doc_type,decoded_data_inside_3):
#     if executive_summary_doc_type == "pdf":
#         file_name_inside = f"{new_room.name.replace(' ', '_')}document.pdf"
#         new_file_inside = frappe.new_doc('File')
#         new_file_inside.file_name = file_name_inside
#         new_file_inside.content = decoded_data_inside_3
#         new_file_inside.attached_to_doctype = "Pitch Room"
#         new_file_inside.attached_to_name = new_room.name
#         new_file_inside.attached_to_field = "executive_summary"
#         new_file_inside.is_private = 0
#         new_file_inside.save(ignore_permissions=True)
#         frappe.db.commit()
#         frappe.db.set_value("Pitch Room",new_room.name,'executive_summary',new_file_inside.file_url)
#     elif executive_summary_doc_type == "xlsx":
#         file_name_inside = f"{new_room.name.replace(' ', '_')}document.xlsx"
#         new_file_inside = frappe.new_doc('File')
#         new_file_inside.file_name = file_name_inside
#         new_file_inside.content = decoded_data_inside_3
#         new_file_inside.attached_to_doctype = "Pitch Room"
#         new_file_inside.attached_to_name = new_room.name
#         new_file_inside.attached_to_field = "executive_summary"
#         new_file_inside.is_private = 0
#         new_file_inside.save(ignore_permissions=True)
#         frappe.db.commit()
#         frappe.db.set_value("Pitch Room",new_room.name,'executive_summary',new_file_inside.file_url)
#     elif executive_summary_doc_type == "docx":
#         file_name_inside = f"{new_room.name.replace(' ', '_')}document.docx"
#         new_file_inside = frappe.new_doc('File')
#         new_file_inside.file_name = file_name_inside
#         new_file_inside.content = decoded_data_inside_3
#         new_file_inside.attached_to_doctype = "Pitch Room"
#         new_file_inside.attached_to_name = new_room.name
#         new_file_inside.attached_to_field = "executive_summary"
#         new_file_inside.is_private = 0
#         new_file_inside.save(ignore_permissions=True)
#         frappe.db.commit()
#         frappe.db.set_value("Pitch Room",new_room.name,'executive_summary',new_file_inside.file_url)    
#     else:
#         return "The Given document is not a Image or PDF"    
        



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
            "profile_image":image_url or "",
            "email_id":profile.email_id,
            "designation":profile.designation or ""
        }
        format_user.append(user_role)
    return {"status":True,"user_role":format_user}
if __name__ == "__main__":
    students_users = get_users_with_role()
    print(f"Users with the role 'Students': {students_users}")


# documents upload for child table
@frappe.whitelist()
def pitch_room_doc_upload(name, pitch_room_documents_upload):
    pitch_room_details = []
    try:
        pitch_room = frappe.get_doc('Pitch Room', name)
        plain_text_short_description = html2text.html2text(pitch_room.about_startup).strip()
        if pitch_room.cover_image:
            image_url = get_domain_name() + pitch_room.cover_image
        else:
            image_url = ""
        pitch_room_detail = {
            'id': pitch_room.name,
            'room_name': pitch_room.room_name,
            "cover_image": image_url,
            'about_startup': plain_text_short_description,
        }
        pitch_room_details.append(pitch_room_detail)
        # Check if the number of existing documents exceeds 10
        if len(pitch_room.pitch_room_documents_upload) + len(pitch_room_documents_upload) > 10:
            return {"status": False, "message": "Cannot upload more than 10 documents.", "pitch_room_details": []}  # Changed here
        for document in pitch_room_documents_upload:
            document_type = document.get("document_type")
            attach = document.get("attach")
            if document_type in ["pdf", "xlsx", "docx"]:
                file_name_inside = f"{pitch_room.name.replace(' ', '_')}document.{document_type}"
                attach_converted_url = base64.b64decode(attach)
                new_file_inside = frappe.new_doc('File')
                new_file_inside.file_name = file_name_inside
                new_file_inside.content = attach_converted_url
                new_file_inside.attached_to_doctype = "Pitch Room"
                new_file_inside.attached_to_name = pitch_room.name
                new_file_inside.attached_to_field = "attach" 
                new_file_inside.is_private = 0
                new_file_inside.save(ignore_permissions=True)
                frappe.db.commit()
                pitch_room.append("pitch_room_documents_upload", {
                    "document_type": document_type,
                    "attach": new_file_inside.file_url
                })
                pitch_room.save(ignore_permissions=True)
                frappe.db.commit()
            else:
                return {"status": False, "message": "The given document type is not supported.", "pitch_room_details": pitch_room_details}
        return {"status": True, "message": "Documents uploaded successfully.", "pitch_room_details": pitch_room_details}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error in pitch room documents upload"))
        return {"status": False, "message": str(e), "pitch_room_details": pitch_room_details}

# pitch room shared user added in child table
@frappe.whitelist()
def shared_user_added(user_id, user_names, pitch_room_id):
    try:
        pitch_room = frappe.get_doc('Pitch Room', pitch_room_id)
        if pitch_room.user_id == user_id:
            for name in user_names:
                user = frappe.get_doc("User", {"first_name": name.strip()})
                if user:
                    pitch_room.append("shared_users", {
                        "user_name": name.strip(),
                        "user_id": user.name
                    })
                else:
                    frappe.log_error(f"User '{name}' not found")

            if pitch_room.get("shared_users"):
                pitch_room.save()
                frappe.db.commit()
                return {"status": True, "message": "Users added successfully"}
            else:
                return {"status": False, "message": "No valid users provided"}
        else:
            return {"status": False, "message": "Unauthorized user for this pitch room"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error in pitch room documents upload"))
        return {"status": False, "message": str(e)}
