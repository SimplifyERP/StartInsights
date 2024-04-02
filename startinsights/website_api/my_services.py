import frappe
from frappe import _
from frappe.utils import now, getdate, today, format_date,format_time
from bs4 import BeautifulSoup
from datetime import datetime

#set the chat coverstations
@frappe.whitelist()
def set_chat_conversation(my_service_id,chat_text):
    try:
        get_my_service = frappe.get_doc("My Services",my_service_id) 
        comment = get_my_service.add_comment("Comment", _(chat_text))
        comment.custom_user = 1
        get_my_service.save()
        comment.save()
        frappe.db.commit()
        return {"status":True,"message":"Comment added successfully"}
    except Exception as e:
        return {"status":False,"message":e}

#get the all chat conversations against the user and service id
@frappe.whitelist()
def get_chat_conversation(service_id,doctype):
    try:
        comments = frappe.db.get_all("Comment",filters={"reference_name":service_id,"reference_doctype":doctype},fields=['content','creation','custom_user'], order_by="creation ASC")
        if comments:
            # Extract comment content and format into chat box format
            chat_boxes = []
            for comment in comments:
                content = comment.get('content')
                custom_user = comment.get('custom_user')
                if content:
                    # Remove HTML tags from the comment content
                    comment_text = BeautifulSoup(content, "html.parser").get_text()
                    # Convert creation timestamp to string
                    creation_timestamp = str(comment.get('creation'))
                    creation_date = format_date(creation_timestamp)
                    creation_time = format_time(creation_timestamp)
                    # Determine the position of the chat box based on custom_user checkbox
                    place = "Right" if custom_user else "Left"
                    chat_boxes.append({
                        "chat_box": comment_text,
                        "chat_date": creation_date,
                        "chate_time": creation_time,
                        "place": place
                    })
            return {"status": True, "chat_conversation":chat_boxes}
        else:
            return {"status":False,"message":"No comments found for the specified document ID."}
    except Exception as e:
        return {"status":False,"message":e}
