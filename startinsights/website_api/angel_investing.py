import frappe
from frappe import _
import html2text
from frappe.utils import  get_url


#course details
@frappe.whitelist()
def angel_investing_details(course_id):
    try:
        if not frappe.db.exists('LMS Course', {'name': course_id}):
            return {"status": False, "message": _("There is no Course in Frappe LMS")}
        courses = frappe.get_all('LMS Course', filters={'name': course_id}, fields=['*'])
        formatted_course = []
        for course in courses:
            course_data = {
                'id': course.name,
                'name': course.name,
                'course_title': course.title,
                'chapters': []
            }
            chapter_details = frappe.get_all('Chapter Reference', filters={'parent': course.name},fields=['chapter'])
            for chapter in chapter_details:
                lesson_details = frappe.get_all('Lesson Reference', filters={'parent': chapter.chapter},fields=['lesson'])
                chapter_data = {
                    'chapter_name': chapter.chapter,
                    'lessons': []
                }
                for lesson in lesson_details:
                    lesson_doc = frappe.get_doc('Course Lesson', lesson.lesson)
                    youtube_video_id = lesson_doc.body.split('/')[-1] 
                    youtube_video = lesson_doc.youtube
                    youtube_link = "https://youtu.be/"
                    lesson_data = {
                        'lesson_name': lesson.lesson,
                        'body': youtube_video
                    }
                    chapter_data['lessons'].append(lesson_data)
                course_data['chapters'].append(chapter_data)
            formatted_course.append(course_data)
        return {"status": True, "course": formatted_course}
    except Exception as e:
        return {"status": False, "message": e}