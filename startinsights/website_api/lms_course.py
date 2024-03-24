from frappe import _
import html2text
from frappe.utils import get_url
import urllib.parse
from urllib.parse import quote
from startinsights.custom import get_domain_name
import frappe


# calculate the page count of given data
def calculate_count(page_count):
    if int(page_count) <= 0:
        return None, None  # Handle invalid page counts
    # Calculate min and max counts
    min_count = (int(page_count) - 1) * 8
    max_count = min_count + 8
    return min_count, max_count   

# Get the customer_group from Profile Application Document
def get_customer_group(user_id):
    profile = frappe.db.get_value('Profile Application', filters={'user_id': user_id}, fieldname='customer_group')
    return profile

# Get the LMS course progress
def get_lms_progress(user_id, lesson_id):
    status = bool(False)
    lms_progress = frappe.db.exists("LMS Course Progress", {'member': user_id, 'lesson': lesson_id, 'status': "Complete"})
    if lms_progress:
        status = bool(True)
    return status

#course videos count
def get_course_videos(lesson_count):
    videos_len = 0
    for lesson in lesson_count:
        videos = frappe.db.get_all("Lesson Reference", {'parent': lesson.chapter}, ['name'], order_by='idx ASC')
        videos_len += len(videos)
    return videos_len

def get_lesson_count(chapter_id):
    lesson_count = frappe.db.count('Lesson Reference', filters={'parent':chapter_id})
    return lesson_count

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

@frappe.whitelist()
def get_chapters_count(course_id):
    chapter_count = frappe.db.count('Chapter Reference', filters={'parent':course_id})
    return chapter_count


#list of courses
@frappe.whitelist()
def learn_list(user_id):
    image_url = ""
    listed_courses = []
    favourite_status = False
    try:
        customer_group = get_customer_group(user_id)
        if customer_group:
            courses_list_api = frappe.db.get_all('LMS Course',{"custom_disabled":0,'custom_customer_group':customer_group},['*'])
        else:
            courses_list_api = frappe.db.get_all('LMS Course',{"custom_disabled":0},['*'])    
        # Format the response
        formatted_course_list = []
        for course_list in courses_list_api:
            learn_favourite = frappe.db.get_value("Learn Favourites",{"user_id":user_id,"course_id":course_list.name},['course_favourite'])
            if learn_favourite == 1:
                favourite_status = True
            else:
                favourite_status = False    
            # Get count of lessons for the current course
            lesson_count = frappe.db.get_all("Chapter Reference", {'parent': course_list.name}, ['chapter'], order_by='idx ASC') 
            videos_count = get_course_videos(lesson_count)
            quiz_count = get_quiz_count(course_list.title)
            if course_list.image:
                image_url = get_domain_name() + course_list.image
            else:
                image_url = ""    
            listed_courses = {
                'id': course_list.name,
                'title': course_list.title,
                "favourite_status":favourite_status,
                'image': image_url,
                'short_introduction': course_list.short_introduction,
                'chapter_count': len(lesson_count),
                'videos_count': videos_count,
                'quiz_count':quiz_count
                
            }
            formatted_course_list.append(listed_courses)
        return {"status": True, "courses_list": formatted_course_list}
    except Exception as e:
        return {"status": False, "message": str(e)}

# Course details
@frappe.whitelist()
def learn_details(course_id, user_id):
    video_url = ""
    lesson_count = 0
    plain_text_description = ""
    try:
        course_list = []
        get_course = frappe.get_doc('LMS Course',course_id)
        plain_text_description = html2text.html2text(get_course.description or "").strip()
        course_data = {
            "id": get_course.name,
            "name": get_course.name,
            "course_title": get_course.title,
            "description": plain_text_description,
            "chapters_count": get_chapters_count(course_id),
            'chapters': []
        }
        # get the chapter wise data
        chapter_details = frappe.db.get_all('Chapter Reference', filters={'parent': get_course.name}, fields=['chapter'], order_by='idx ASC')
        for chapter in chapter_details:
            lesson_count = get_lesson_count(chapter.chapter)
            lesson_details = frappe.db.get_all('Lesson Reference', filters={'parent': chapter.chapter}, fields=['lesson'], order_by='idx ASC')
            chapter_data = {
                "chapter_name": chapter.chapter,
                "lesson_count":lesson_count,
                "lessons": []
            }
            for lesson in lesson_details:
                lms_course_progress = get_lms_progress(user_id, lesson.lesson)
                lesson_doc = frappe.get_doc('Course Lesson', lesson.lesson)
                if lesson_doc.custom_video:
                    video_url = get_domain_name() + lesson_doc.custom_video
                else:
                    video_url = ""
                encoded_url = quote(video_url)
                lesson_data = {
                    'lesson_name': lesson.lesson,
                    'body': encoded_url,
                    'course_seen_status': lms_course_progress,
                    'extension': lesson_doc.custom_extension_type
                }
                chapter_data["lessons"].append(lesson_data)
            course_data["chapters"].append(chapter_data)
        course_list.append(course_data)
        return {"status":True,"course_details":course_list}
    except Exception as e:
        return {"status":False,"message":e}    

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

@frappe.whitelist()
def mark_favourite_course(user_id,course_id):
    status = False
    message = ""
    try:
        if not frappe.db.exists("Learn Favourites",{"user_id":user_id,"course_id":course_id}):
            new_favourite_course = frappe.new_doc("Learn Favourites")
            new_favourite_course.user_id = user_id
            new_favourite_course.course_id = course_id
            new_favourite_course.course_favourite = 1
            new_favourite_course.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("Learn Favourites",new_favourite_course.name,'owner',user_id)
            status = True
            message = "Favourite Successfully"
        else:
            favourite_course = frappe.db.get_value("Learn Favourites",{"user_id":user_id,"course_id":course_id},['name'])
            update_favourite_course = frappe.get_doc("Learn Favourites",favourite_course)
            update_favourite_course.course_favourite = 1
            update_favourite_course.save(ignore_permissions=True)
            frappe.db.commit()   
            status = True
            message = "Favourite Successfully"
        return {"status":status,"message":message}
    except Exception as e:
        return {"status":False,"message":e}

@frappe.whitelist()
def unmarked_favourite_course(user_id,course_id,status):
    try:
        favourite_course = frappe.db.get_value("Learn Favourites",{"user_id":user_id,"course_id":course_id},['name'])
        frappe.db.set_value("Learn Favourites",favourite_course,"course_favourite",status)
        return {"status":True,"message":"Un Marked Favourite"}
    except Exception as e:
        return {"status":False,"message":e}

@frappe.whitelist()
def get_favourite_courses(user_id,status):
    image_url = ""
    try:
        learn_list = []
        # page_no_calulate = calculate_count(page_no)
        favourite_course_list = frappe.db.sql(""" SELECT course_id FROM `tabLearn Favourites` WHERE user_id = %s AND course_favourite = %s  ORDER BY name ASC  """, (user_id,status), as_dict=True)
        for course in favourite_course_list:
            get_course_details = frappe.get_doc("LMS Course",course.course_id)

            lesson_count = frappe.db.get_all("Chapter Reference", {'parent': get_course_details.name}, ['chapter'], order_by='idx ASC')
            videos_count = get_course_videos(lesson_count)
            quiz_count = get_quiz_count(get_course_details.title)
            if get_course_details.image:
                image_url = get_domain_name() + get_course_details.image
            else:
                image_url = ""    
            listed_courses = {
                'id': get_course_details.name,
                'title': get_course_details.title,
                "favourite_status":True,
                'image': image_url,
                'short_introduction': get_course_details.short_introduction,
                'chapter_count': len(lesson_count),
                'videos_count': videos_count,   
                'quiz_count':quiz_count
                
            }
            learn_list.append(listed_courses)
        return {"status":True,"courses_list":learn_list}
    except Exception as e:
        return {"status":False,"message":e}

@frappe.whitelist()
def get_favourite_course_details(user_id,course_id):
    video_url = ""
    lesson_count = 0
    plain_text_description = ""
    try:
        course_list = []
        favourite_course = frappe.db.get_value("Learn Favourites",{"user_id":user_id,"course_id":course_id},['name'])
        if favourite_course:
            get_course = frappe.get_doc('LMS Course',course_id)
            plain_text_description = html2text.html2text(get_course.description or "").strip()
            
            course_data = {
                "id": get_course.name,
                "name": get_course.name,
                "course_title": get_course.title,
                "description": plain_text_description,
                "chapters_count": get_chapters_count(course_id),
                'chapters': []
            }
            # get the chapter wise data
            chapter_details = frappe.db.get_all('Chapter Reference', filters={'parent': get_course.name}, fields=['chapter'], order_by='idx ASC')
            for chapter in chapter_details:
                lesson_count = get_lesson_count(chapter.chapter)
                lesson_details = frappe.db.get_all('Lesson Reference', filters={'parent': chapter.chapter}, fields=['lesson'], order_by='idx ASC')
                chapter_data = {
                    "chapter_name": chapter.chapter,
                    "lesson_count":lesson_count,
                    "lessons": []
                }
                for lesson in lesson_details:
                    lms_course_progress = get_lms_progress(user_id, lesson.lesson)
                    lesson_doc = frappe.get_doc('Course Lesson', lesson.lesson)
                    if lesson_doc.custom_video:
                        video_url = get_domain_name() + lesson_doc.custom_video
                    else:
                        video_url = ""
                    encoded_url = quote(video_url)
                    lesson_data = {
                        'lesson_name': lesson.lesson,
                        'body': encoded_url,
                        'status': lms_course_progress,
                        'extension': lesson_doc.custom_extension_type
                    }
                    chapter_data["lessons"].append(lesson_data)
                course_data["chapters"].append(chapter_data)
            course_list.append(course_data)
        return {"status":True,"favourite_course_detail":course_list}
    except Exception as e:
        return {"status":False,"message":e}    


