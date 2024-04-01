import frappe
from frappe import _
from frappe.utils import now, getdate, today, format_date,format_time


@frappe.whitelist()
def add_comment_to_service(service_name, comment_text):
    try:
        service_doc = frappe.get_doc("My Services", service_name) 
        comment = service_doc.add_comment("Comment", _(comment_text))
        comment.custom_user = 1
        service_doc.save()
        comment.save()
        frappe.db.commit()
        return "Comment added successfully"
    
    except Exception as e:
        return f"Error: {e}"


import frappe
from bs4 import BeautifulSoup
from datetime import datetime

@frappe.whitelist()
def get_all_comments(doc_id, doc_name):
    try:
        # Fetch all comments for the given document
        comments = frappe.db.get_all("Comment", filters={"reference_name": doc_id, "reference_doctype": doc_name}, fields=['content', 'creation', 'custom_user'], order_by="creation ASC")

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
                        "created_date": creation_date,
                        "created_time": creation_time,
                        "place": place
                    })

            return {"status": True, "comments": chat_boxes}
        else:
            return {"status": False, "message": "No comments found for the specified document ID."}
    except Exception as e:
        print("Error fetching comments:", e)
        return {"status": False, "message": f"Error fetching comments: {str(e)}"}
