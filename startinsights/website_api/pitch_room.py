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
def get_room_details(user_id):
    doc_url = ""
    image_url = ""
    company_name = ""
    try:
        get_pitch_room = frappe.db.get_all('Pitch Room',{'user_id':user_id},['name','room_name','cover_image','about_startup'], order_by='idx ASC')
        get_pitch_room_list = []
        get_pitch_room_list.append(get_pitch_room_details_empty())
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
                "id": pitch_room.name,
                "cover_image":image_url,
                "room_name": pitch_room.room_name,
                "company_name":company_name,
                "about_startup": pitch_room.about_startup or "",
                "notes":pitch_room.notes or "",
                "documents":[],
                "shared_users":[]
            }
            #get the documents upload child table list
            get_documents = frappe.db.get_all("Pitch Craft Document Table",{'parent':pitch_room.name},['document_type','attach'],order_by='idx ASC')
            for documents in get_documents:
                if documents.attach:
                    doc_url = get_domain_name() + documents.attach
                else:
                    doc_url = ""    
                pitch_room_details["documents"].append({
                    "document_type":documents.document_type,
                    "attach": doc_url
                })
            get_share_users = frappe.db.get_all("Shared Users",{'parent':pitch_room.name},['user_id','user_name'],order_by='idx ASC')
            for users in get_share_users:
                pitch_room_details["shared_users"].append({
                    "user_id":users.user_id,
                    "user_name": users.user_name
                })    

            
            get_pitch_room_list.append(pitch_room_details)

        if not get_pitch_room_list:  # If the list is empty, add default details
            get_pitch_room_list.append(get_pitch_room_details_empty())
            
        return {"status": True, "pitch_room_details":get_pitch_room_list}
    except Exception as e:
        return {"status": False,"message":e}

#first given dict will be empty
def get_pitch_room_details_empty():
    pitch_room_details = {
        'id':"",
        "cover_image":"",
        'room_name':"",
        'company_name':"",
        'about_startup':"",
        "notes":"",
        "documents":[],
        "shared_users":[]
    }
    return pitch_room_details

# documents upload for child table
@frappe.whitelist()
def pitch_room_doc_upload(room_id,pitch_room_documents,notes):
    pitch_room_details = []
    try:
        pitch_room = frappe.get_doc('Pitch Room',room_id)
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
        if len(pitch_room.pitch_room_documents_upload) + len(pitch_room_documents) > 10:
            return {"status": False, "message": "Cannot upload more than 10 documents.", "pitch_room_details": []}  # Changed here
        for document in pitch_room_documents:
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
                pitch_room.notes = notes
                pitch_room.save(ignore_permissions=True)
                frappe.db.commit()
            else:
                return {"status": False, "message": "The given document type is not supported.", "pitch_room_details": pitch_room_details}
        return {"status": True, "message": "Documents uploaded successfully.", "pitch_room_details": pitch_room_details}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error in pitch room documents upload"))
        return {"status": False, "message": str(e), "pitch_room_details": pitch_room_details}


#shared user id append in child table 

@frappe.whitelist()
def shared_user(user_ids, notes, pitch_room_id):
    try:
        pitch_room = frappe.get_doc('Pitch Room', pitch_room_id)
        for user_id in user_ids:
            user = frappe.get_doc("User", {"email": user_id.strip()})
            if user:
                pitch_room.append("shared_users", {
                    "user_id": user_id.strip(),
                })
            else:
                return {"status": False, "message": "User with ID '{user_id}' not found"}
        pitch_room.notes = notes
        if pitch_room.get("shared_users"):
            pitch_room.save()
            frappe.db.commit()
            return {"status": True, "message": "Users added successfully"}
        else:
            return {"status": False, "message": "No valid users provided"}

    except Exception as e:
        return {"status": False, "message": str(e)}


@frappe.whitelist()
def get_users_with_role():
    user_type = "Investors"
    image_url = ""
    get_profile_details = frappe.db.get_all("Profile Application",{"customer_group":user_type},['*'])
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
