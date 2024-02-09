import frappe

@frappe.whitelist()
def get_quiz(lesson_id):
    try:
        get_lesson = frappe.db.get_all("Course Lesson",{'name':lesson_id},['*'])
        return {"status":True,"quiz":get_lesson}
    except Exception as e:
        return {"status":False,"message":e}