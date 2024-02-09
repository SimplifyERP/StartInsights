import frappe
from lms.lms.doctype.course_lesson.course_lesson import CourseLesson


class CustomCourseLesson(CourseLesson):
    def before_save(self):
        for quiz in self.custom_quiz_table:
            frappe.db.set_value("LMS Quiz",quiz.quiz,'custom_quiz_attempts',str(quiz.attempts) + " Attempt")
            frappe.db.set_value("LMS Quiz",quiz.quiz,'custom_course_lesson',self.name)      
        

