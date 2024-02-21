import frappe
from frappe.utils import get_url
import html2text
import base64
from frappe.utils.file_manager import save_file


# Creating a new pitch room list
@frappe.whitelist()
def create_pitch_room(room_name, description,pitch_deck,projections,executive_summary,doc_type,shared_user):
    try:
        decoded_data_inside_1 = base64.b64decode(pitch_deck)
        decoded_data_inside_2 = base64.b64decode(projections)
        decoded_data_inside_3 = base64.b64decode(executive_summary)
        #creating a new pitch room through api
        new_room = frappe.new_doc('Pitch Room')
        new_room.room_name = room_name
        new_room.description = description
        new_room.shared_user = shared_user
        new_room.save(ignore_permissions=True)
        frappe.db.commit()
        # the below method the giving the pitch deck attach in file list
        attach_pitch_deck(new_room,doc_type,decoded_data_inside_1)
        #the below method the giving the projections attach in file list
        attach_projections(new_room,doc_type,decoded_data_inside_2)
        #the below method the giving the executive_summary attach in file list
        attach_executive_summary(new_room,doc_type,decoded_data_inside_3)
        return {'status':True,"message":"New Pitch Room Created"}
    except Exception as e:
        status = False
        return {'status': status, 'message': str(e)}

def attach_pitch_deck(new_room,doc_type,decoded_data_inside_1):
    if doc_type == "Image":
        file_name_inside = f"{new_room.name.replace(' ', '_')}_image.png"
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
    elif doc_type == "Pdf":
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
    else:
        return "The Given document is not a Image or PDF"    

def attach_projections(new_room,doc_type,decoded_data_inside_2):
    if doc_type == "Image":
        file_name_inside = f"{new_room.name.replace(' ', '_')}_image.png"
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
    elif doc_type == "Pdf":
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
    else:
        return "The Given document is not a Image or PDF"
    
def attach_executive_summary(new_room,doc_type,decoded_data_inside_3):
    if doc_type == "Image":
        file_name_inside = f"{new_room.name.replace(' ', '_')}_image.png"
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
    elif doc_type == "Pdf":
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
            plain_text_description = html2text.html2text(pitch_room.description).strip()

            doc_1 = get_url() + pitch_room.document_1 if pitch_room.document_1 else ""
            doc_2 = get_url() + pitch_room.document_2 if pitch_room.document_2 else ""
            doc_3 = get_url() + pitch_room.document_3 if pitch_room.document_3 else ""

            pitch_room_details = {
                'id': pitch_room.name,
                'room_name': pitch_room.room_name,
                'description': plain_text_description,
                'pitch_deck': doc_1,
                'projections': doc_2,
                'executive_summary': doc_3,
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
                doc_1 = get_url() + room.document_1
            else:
                doc_1 = ""

            if room.projections:
                doc_2 = get_url() + room.document_2
            else:
                doc_2 = "" 

            if room.executive_summary:
                doc_3 = get_url() + room.document_3
            else:
                doc_3 = ""  
            room_list = {
                "name":room.room_name,
                "room_name":room.room_name,
                "description":description or '',
                "pitch_deck":doc_1,
                "projections":doc_2,
                "executive_summary":doc_3,                
            }
            formatted_pitch_room.append(room_list)
        return {"status":True,"pitch_room":formatted_pitch_room}
    except Exception as e:
        return {"status":False,"message":e}

@frappe.whitelist()
def get_users_with_role():
    role = "Investors"
    users_with_role = frappe.get_all("Has Role", filters={"role": role}, fields=["parent"])
    user_list = [user.get("parent") for user in users_with_role]
    return user_list
if __name__ == "__main__":
    students_users = get_users_with_role()
    print(f"Users with the role 'Students': {students_users}")
