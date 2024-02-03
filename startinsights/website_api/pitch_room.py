import frappe
from frappe.utils import get_url
import html2text
import base64



# Creating a new pitch room list
@frappe.whitelist()
def create_pitch_room(room_name, description,document_1,document_2,document_3,document_4):
    status = "True"
    message = "Pitch Room Created"
    try:
        decoded_data_inside_1 = base64.b64decode(document_1)
        decoded_data_inside_2 = base64.b64decode(document_2)
        decoded_data_inside_3 = base64.b64decode(document_3)
        decoded_data_inside_4 = base64.b64decode(document_4)
        new_room = frappe.new_doc('Pitch Room')
        new_room.room_name = room_name
        new_room.description = description
        new_room.document_1 = decoded_data_inside_1
        new_room.document_2 = decoded_data_inside_2
        new_room.document_3 = decoded_data_inside_3
        new_room.document_4 = decoded_data_inside_4
        new_room.save(ignore_permissions=True)
        frappe.db.commit()

      
        return {'status': status,"message":message}
    except Exception as e:
        status = False
        return {'status': status, 'message': str(e)}
    


# pitch room details view
@frappe.whitelist()
def pitch_room_list():
    try:
        pitch_room_list = frappe.db.get_all('Pitch Room', ['name', 'room_name', 'description', 'document_1', 'document_2', 'document_3', 'document_4'], order_by='idx ASC')
        formatted_pitch_room_list = []

        for pitch_room in pitch_room_list:
            plain_text_description = html2text.html2text(pitch_room.description).strip()

            document_1 = get_url() + pitch_room.document_1 if pitch_room.document_1 else ""
            document_2 = get_url() + pitch_room.document_2 if pitch_room.document_2 else ""
            document_3 = get_url() + pitch_room.document_3 if pitch_room.document_3 else ""
            document_4 = get_url() + pitch_room.document_4 if pitch_room.document_4 else ""

            pitch_room_details = {
                'id': pitch_room.name,
                'room_name': pitch_room.room_name,
                'description': plain_text_description,
                'document_1': document_1,
                'document_2': document_2,
                'document_3': document_3,
                'document_4': document_4
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
            if room.document_1:
                doc_1 = get_url() + room.document_1
            else:
                doc_1 = ""

            if room.document_2:
                doc_2 = get_url() + room.document_2
            else:
                doc_2 = "" 

            if room.document_3:
                doc_3 = get_url() + room.document_3
            else:
                doc_3 = ""  

            if room.document_4:
                doc_4 = get_url() + room.document_4
            else:
                doc_4 = "" 
            room_list = {
                "name":room.room_name,
                "room_name":room.room_name,
                "description":description or '',
                "document_1":doc_1,
                "document_2":doc_2,
                "document_3":doc_3,
                "document_4":doc_4,
                
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
