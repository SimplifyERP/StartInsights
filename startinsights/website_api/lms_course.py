import frappe
from frappe import _
import html2text
from frappe.utils import  get_url
import urllib.parse
from urllib.parse import quote

# course details
@frappe.whitelist()
def lms_course_details(course_id,user_id):
    video_url = ""
    plain_text_description = ""
    try:
        if not frappe.db.exists('LMS Course', {'name': course_id}):
            return {"status": False, "message": _("There is no Course in Frappe LMS")}
        courses = frappe.get_all('LMS Course', filters={'name': course_id}, fields=['*'])
        formatted_course = []
        for course in courses:
            # Convert HTML description to plain text
            plain_text_description = html2text.html2text(course.description).strip()
            course_data = {
                'id': course.name,
                'name': course.name,
                'course_title': course.title,
                'description': plain_text_description,
                'chapters': []
            }
            chapter_details = frappe.get_all('Chapter Reference', filters={'parent': course.name}, fields=['chapter'], order_by='idx ASC')
            for chapter in chapter_details:
                lesson_details = frappe.get_all('Lesson Reference', filters={'parent': chapter.chapter}, fields=['lesson'], order_by='idx ASC')
                chapter_data = {
                    'chapter_name': chapter.chapter,
                    'lessons': []
                }
                for lesson in lesson_details:
                    lms_course_progress = get_lms_progress(user_id,lesson.lesson)
                    lesson_doc = frappe.get_doc('Course Lesson', lesson.lesson)
                    if lesson_doc.custom_video:
                        video_url = get_url() + lesson_doc.custom_video
                    else:
                        video_url = ""   
                    
                    encoded_url = quote(video_url)
                    lesson_data = {
                        'lesson_name': lesson.lesson,
                        'body': encoded_url,
                        'status':lms_course_progress
                    }
                    chapter_data['lessons'].append(lesson_data)
                course_data['chapters'].append(chapter_data)
            formatted_course.append(course_data)
        return {"status": True, "Course": formatted_course}
    except Exception as e:
        return {"status": False, "message": str(e)}

#get the lms course progress
def get_lms_progress(user_id,lesson_id):
    status = bool(False)
    lms_progress = frappe.db.exists("LMS Course Progress",{'member':user_id,'lesson':lesson_id,'status':"Complete"})
    if lms_progress:
        status = bool(True)
    else:
        status
    return status    

#list of courses
@frappe.whitelist()
def courses_list_api():
    image_url = ""
    listed_courses = []
    saved_courses_list = []
    try:
        courses_list_api = frappe.db.get_all('LMS Course',{'custom_course_status':"Unsaved"},['*'])
        # Format the response
        formatted_course_list = []
        for course_list in courses_list_api:
            # Get count of lessons for the current course
            lesson_count = frappe.db.get_all("Chapter Reference", {'parent': course_list.name}, ['chapter'], order_by='idx ASC')
            videos_count = get_course_videos(lesson_count)
            quiz_count = get_quiz_count(course_list.title)
            if course_list.image:
                image_url = get_url() + course_list.image
            else:
                image_url = ""    
            listed_courses = {
                'id': course_list.name,
                'title': course_list.title,
                'image': image_url,
                'short_introduction': course_list.short_introduction,
                'lesson_count': len(lesson_count),
                'quiz_count':quiz_count,
                'videos_count': videos_count   
            }
            formatted_course_list.append(listed_courses)
        saved_courses_list = get_saved_courses_list()
        return {"status": True, "courses_list": formatted_course_list,"saved_courses":saved_courses_list}
    except Exception as e:
        return {"status": False, "message": str(e)}
        
def get_saved_courses_list():
    image_url = ""
    saved_courses = []
    try:
        get_saved_courses = frappe.db.get_all('LMS Course',{'custom_course_status':"Saved"},['*'])
        # Format the response
        formatted_saved_courses = []
        for course_list in get_saved_courses:
            # Get count of lessons for the current course
            lesson_count = frappe.db.get_all("Chapter Reference", {'parent': course_list.name}, ['chapter'], order_by='idx ASC')
            videos_count = get_course_videos(lesson_count)
            quiz_count = get_quiz_count(course_list.title)
            if course_list.image:
                image_url = get_url() + course_list.image
            else:
                image_url = ""    
            saved_courses = {
                'id': course_list.name,
                'title': course_list.title,
                'image': image_url,
                'short_introduction': course_list.short_introduction,
                'lesson_count': len(lesson_count),
                'quiz_count':quiz_count,
                'videos_count': videos_count   
            }
            formatted_saved_courses.append(saved_courses)
        return formatted_saved_courses
    except Exception as e:
        return {"message": str(e)}        

#course videos count
def get_course_videos(lesson_count):
    videos_len = 0
    for lesson in lesson_count:
        videos = frappe.db.get_all("Lesson Reference", {'parent': lesson.chapter}, ['name'], order_by='idx ASC')
        videos_len += len(videos)
    return videos_len

#quiz videos count
def get_quiz_count(course_title):
    quiz_count = 0
    get_course_id = frappe.db.get_value("LMS Course",{'title':course_title},['name'])
    if get_course_id:
        get_quiz_count = frappe.db.count('LMS Quiz', filters={'course': get_course_id})
        quiz_count = get_quiz_count
        return get_quiz_count
    else:
        quiz_count = 0
        return quiz_count

#get the saved and unsaved courses list
@frappe.whitelist()
def get_saved_list_course(course_id,status):
    message = ""
    try:
        if status:
            frappe.db.set_value("LMS Course",course_id,'custom_course_status',status)
            message = "%s course update as %s"%(course_id,status)
            return {"status": True, "message":message} 
        else:
            message = "Please Put the Status"
            return {"status": False, "message":message} 
    except Exception as e:
        return {"status": False, "message": str(e)}
    
#create a lms course progress for user completed the lesson
@frappe.whitelist()
def create_lms_progress(user_id,lesson_id,status):
    try:
        if not frappe.db.exists("LMS Course Progress",{'member':user_id,'lesson':lesson_id}):
            new_lms_progress = frappe.new_doc("LMS Course Progress")
            new_lms_progress.member = user_id
            new_lms_progress.status = status
            new_lms_progress.lesson = lesson_id
            new_lms_progress.save(ignore_permissions=True)
            frappe.db.commit()
            return {"status":True,"message":"New LMS Progress Created"}
        else:    
            return {"status":False,"message":"Already User have Progress for the lesson"}
    except Exception as e:
        return {"status":False,"message":e}