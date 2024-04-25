import frappe
from frappe.utils import get_url
import html2text
import base64
from frappe.utils.file_manager import save_file
from datetime import datetime
from frappe.utils import now, getdate, today, format_date,format_time
from startinsights.custom import get_domain_name
from frappe import _, get_doc
import json


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

            file_name_inside = f"{pitch_room_name.replace(' ', '_')}cover_imgae.jpg"
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
        get_pitch_room = frappe.db.get_all('Pitch Room',{"user_id":user_id},['name','room_name','cover_image','about_startup'], order_by='idx ASC')
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
                "notes":get_room_notes() or "",
                "documents":[],
                "shared_users":[]
            }
            #get the documents upload child table list
            get_documents = frappe.db.get_all("Pitch Craft Document Table",{'parent':pitch_room.name},['name','doc_name','document_type','attach'],order_by='idx ASC')
            for documents in get_documents:
                get_file = frappe.db.get_value("File",{"attached_to_doctype":"Pitch Room","attached_to_name":pitch_room.name},['creation'])
                if documents.attach:
                    doc_url = get_domain_name() + documents.attach
                else:
                    doc_url = ""    
                pitch_room_details["documents"].append({
                    "doc_id":documents.name,
                    "doc_name":documents.doc_name or "",
                    "document_type":documents.document_type,
                    "attach": doc_url,
                    "is_upload":True,
                    "created_date":format_date(get_file.date()),
                    "created_time":change_time_format(format_time(get_file)),
                })
            get_share_users = frappe.db.get_all("Shared Users",{'parent':pitch_room.name},['user_id','user_name'],order_by='idx ASC')
            for users in get_share_users:
                pitch_room_details["shared_users"].append({
                    "user_id":users.user_id,
                    "user_name": users.user_name or ""
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
def pitch_room_update(room_id,room_name,about_startup,cover_image,upload_doc,users_shared):
    status = ""
    message = ""
    doc_table_count = 0
    try:
        decode_json_users = json.loads(users_shared)
        decode_doc_json = json.loads(upload_doc)
        base64_to_image = base64.b64decode(cover_image)

        get_room = frappe.get_doc("Pitch Room",room_id)
        get_room.room_name = room_name
        get_room.about_startup = about_startup
        get_room.set("shared_users",[])
        for user in decode_json_users:
            get_room.append("shared_users",{
                "user_id":user.get("user_id")
            })
        get_room.save(ignore_permissions=True)
        frappe.db.commit()
        
        status = True
        message = "Room Updated"

        if base64_to_image:
            file_name_inside = f"{room_name.replace(' ', '_')}cover_imgae.jpg"
            new_file_inside = frappe.new_doc('File')
            new_file_inside.file_name = file_name_inside
            new_file_inside.content = base64_to_image
            new_file_inside.attached_to_doctype = "Pitch Room"
            new_file_inside.attached_to_name = get_room.name
            new_file_inside.attached_to_field = "cover_image"
            new_file_inside.is_private = 0
            new_file_inside.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("Pitch Room",get_room.name,'cover_image',new_file_inside.file_url)

        if not decode_doc_json == []:
            doc_table_count = (len(get_room.pitch_room_documents_upload) + len(upload_doc))
            if doc_table_count > 10:
                for document in decode_doc_json:
                    document_type = document.get("document_type")
                    doc_name = document.get("name")
                    attach = document.get("attach")
                    if document_type in ["pdf","docx","doc","xlsx","png","jpg","jpeg"]:
                        file_name_inside = doc_name
                        attach_converted_url = base64.b64decode(attach)
                        new_file_inside = frappe.new_doc('File')
                        new_file_inside.file_name = file_name_inside
                        new_file_inside.content = attach_converted_url
                        new_file_inside.attached_to_doctype = "Pitch Room"
                        new_file_inside.attached_to_name = room_id
                        new_file_inside.attached_to_field = "attach" 
                        new_file_inside.is_private = 0
                        new_file_inside.save(ignore_permissions=True)
                        frappe.db.commit()
                        
                        doc_upload_room = frappe.get_doc("Pitch Room",room_id)
                        doc_upload_room.append("pitch_room_documents_upload",{
                            "document_type":document_type,
                            "doc_name":doc_name,
                            "attach":new_file_inside.file_url
                        })
                        doc_upload_room.save(ignore_permissions=True)
                        frappe.db.commit()
                        status = True
                        message = "Room Updated"
                    else:
                        status = False
                        message = "The given document type is not supported"    
            else:
                status = False
                message = "File limit is 10 Please remove extra files"
        else:
            message = "Room updated Successfully"           
        return {"status":status,"message":message}
    except Exception as e:
        return {"status": False, "message": str(e)}


#shared user id append in child table 
@frappe.whitelist()
def shared_user(user_ids, pitch_room_id):
    try:
        decode_user_id = json.loads(user_ids)
        pitch_room = frappe.get_doc('Pitch Room', pitch_room_id)
        for user in decode_user_id:
            pitch_room.append("shared_users",{
                "user_id":user.get("user_id")
            })
        pitch_room.save(ignore_permissions=True)
        frappe.db.commit()
        return {"status":True,"messsage":"Room Shared Successfully"}
    except Exception as e:
        return {"status": False, "message": str(e)}

@frappe.whitelist()
def get_users_with_role(pitch_room_id):
    user_type = "Investors"
    image_url = ""
    get_profile_details = frappe.db.get_all("Profile Application", {"customer_group": user_type}, ['*'])
    format_user = []
    for profile in get_profile_details:
        exclude_user = False 
        get_shared_users = frappe.db.get_all("Shared Users", {'parent': pitch_room_id}, ["user_id"])
        for share_users in get_shared_users:
            if share_users.user_id == profile.name:
                exclude_user = True
                break
        if not exclude_user:
            if profile.profile_image:
                image_url = get_domain_name() + profile.profile_image
            else:
                image_url = ""       
            user_role = {
                "user_id": profile.user_id,
                "full_name": profile.full_name,
                "profile_image": image_url or "",
                "email_id": profile.email_id or "",
                "designation": profile.designation or ""
            }
            format_user.append(user_role)
    return {"status": True, "user_role": format_user}

if __name__ == "__main__":
    students_users = get_users_with_role()
    print(f"Users with the role 'Students': {students_users}")


#upload document removed method
@frappe.whitelist()
def remove_document(room_id,doc_id):
    try:
        parent_doc = frappe.get_doc("Pitch Room",room_id)
        child_table_entries = parent_doc.get("pitch_room_documents_upload")
        for entry in child_table_entries:
            if entry.get("name") == doc_id:
                child_table_entries.remove(entry)
                break
        parent_doc.set("pitch_room_documents_upload", child_table_entries)
        parent_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"status":True,"message":"Document Removed"}
    except Exception as e:
        return {"status":False,"message":e}


@frappe.whitelist()
def delete_pitch_room(pitch_room_id,delete_status):
    status = ""
    message = ""
    try:
        if frappe.db.exists("Pitch Room",{"name":pitch_room_id}):
            get_pitch_room = frappe.get_doc("Pitch Room",pitch_room_id)
            get_pitch_room.disabled = delete_status
            get_pitch_room.save(ignore_permissions=True)
            frappe.db.commit()
            status = True
            message = "Success"
        else:
            status = False
            message = "No Pitch Room In Database"
        return {"status":status,"message":message}
    except Exception as e:
        return {"status":False,"message":e}


@frappe.whitelist()
def get_pitch_room_quotes():
    try:
        get_quotes = frappe.get_single("Pitch Room Quote")
        quotes = []
        for quote in get_quotes.quote_table:
            quotes_list  = {
                "quote":quote.quote
            }
            quotes.append(quotes_list)
        return {"status":True,"quotes_list":quotes}
    except Exception as e:
        return {"status":False,"message":str(e)}


# @frappe.whitelist()
# def get_pitch_room_share_list(pitch_room_id):
#     doc_url = ""
#     image_url = ""
#     company_name = ""
#     try:
#         get_pitch_room = frappe.db.get_all('Pitch Room',{'name':pitch_room_id},['*'], order_by='idx ASC')
#         get_pitch_room_list = []
#         for room in get_pitch_room:
#             get_company_name = frappe.db.get_value("Profile Application",{'user_id':room.user_id},['company_name'])
#             if get_company_name:
#                 company_name = get_company_name
#             else:
#                 company_name = ""    

#             if room.cover_image:
#                 image_url = get_domain_name() + room.cover_image
#             else:
#                 image_url = ""

#             pitch_room_details = {
#                 "id": room.name,
#                 "cover_image":image_url,
#                 "room_name": room.room_name,
#                 "company_name":company_name,
#                 "about_startup": room.about_startup or "",
#                 "notes": get_room_notes() or "",
#                 "documents":[],
#                 "shared_users":[]
#             }

#             get_documents = frappe.db.get_all("Pitch Craft Document Table",{'parent':room.name},['name','doc_name','document_type','attach'],order_by='idx ASC')
#             for documents in get_documents:
#                 #the below to get the file creation date and tie
#                 get_file = frappe.db.get_value("File",{"attached_to_doctype":"Pitch Room","attached_to_name":room.name},['creation'])
#                 #the below method is to get the session 
#                 if documents.attach:
#                     doc_url = get_domain_name() + documents.attach
#                 else:
#                     doc_url = ""    
#                 pitch_room_details["documents"].append({
#                     "doc_id":documents.name,
#                     "doc_name":documents.doc_name,
#                     "document_type":documents.document_type,
#                     "attach": doc_url,
#                     "is_upload":True,
#                     "created_date":format_date(get_file),
#                     "created_time":change_time_format(format_time(get_file)),
#                 })

#             get_share_users = frappe.db.get_all("Shared Users",{'parent':room.name},['user_id','user_name'],order_by='idx ASC')
#             for users in get_share_users:
#                 pitch_room_details["shared_users"].append({
#                     "user_id":users.user_id,
#                     "user_name": users.user_name
#                 })    

#             get_pitch_room_list.append(pitch_room_details)
#         return {"status":True,"pitch_room_details":get_pitch_room_list}    
#     except Exception as e:
#         return {"status":False,"message":e}
    
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

#get the room notes by default for all
def get_room_notes():
    notes  = frappe.db.get_single_value("Pitch Room Notes","pitch_room_notes")
    return notes

#time change to 24 Hr to 12 Hr
def change_time_format(time_change):
    time_obj = datetime.strptime(time_change, "%H:%M")    
    time_12hr = time_obj.strftime("%I:%M %p")
    return time_12hr
