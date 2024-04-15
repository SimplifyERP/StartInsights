
import frappe
import html2text
# @frappe.whitelist()
# def get_quiz(lesson_id):
#     try:
#         get_lesson = frappe.db.get_all("Course Lesson",{'name':lesson_id},['*'])
#         return {"status":True,"quiz":get_lesson}
#     except Exception as e:
#         return {"status":False,"message":e}



import html2text
import frappe

@frappe.whitelist()
def get_fund_quiz():
	try:
		fund_quizzes = frappe.db.get_all("Fundability Quiz", ['*'])
		formatted_fund_quizzes = []
		
		for fund_quiz in fund_quizzes:
			question = html2text.html2text(fund_quiz.question or "").strip()
			if fund_quiz.type == "Multi select":
				fund_quiz_details = {
					"id": fund_quiz.name,
					"quiz_question": question,
					"quiz_type": fund_quiz.type,
					"choice_1": fund_quiz.select_1,
					"choice_2": fund_quiz.select_2,
					"choice_3": fund_quiz.select_3,
					"choice_4": fund_quiz.select_4,
					"choice_5": fund_quiz.select_5,

				}
			elif fund_quiz.type == "Choices":
				fund_quiz_details = {
					"id": fund_quiz.name,
					"quiz_question": question,
					"quiz_type": fund_quiz.type,
					"choice_1": fund_quiz.option_1,
					"choice_2": fund_quiz.option_2,
					"choice_3": fund_quiz.option_3,
					"choice_4": fund_quiz.option_4,
				}
			else:
				fund_quiz_details = {
					"id": fund_quiz.name,
					"quiz_question": question,
					"quiz_type": fund_quiz.type,
					"select_1": fund_quiz.display_1,
					"select_2": fund_quiz.display_2,
					"show": [
						{
							"choice_1": getattr(fund_quiz, "display2_select_1"),
							"choice_2": getattr(fund_quiz, "display2_select_2"),
							"choice_3": getattr(fund_quiz, "display2_select_3"),
						}
					],
					"select_3": fund_quiz.display_3,
					"show1": [
						{
							"choice_1": getattr(fund_quiz, "display3_select_1"),
							"choice_2": getattr(fund_quiz, "display3_select_2"),    
							"choice_3": getattr(fund_quiz, "display3_select_3"),
						}
					]
				}
			formatted_fund_quizzes.append(fund_quiz_details)

		return {"status": True, "fundability_quiz": formatted_fund_quizzes}
	except Exception as e:
		return {"status": False, "message": str(e)}


@frappe.whitelist()
def response_details(data):
	try:
		fund_response = frappe.new_doc("Fundability Quiz Response")
		response_marks = []
		for entry in data:
			quiz_id = entry.get("quiz_id")
			single_choice = entry.get("single_choice", None)
			multi_choice = entry.get("multi_choice", None)
			quiz_doc = frappe.get_doc("Fundability Quiz", quiz_id)
			marks = 0
			if single_choice is not None:
				mark_attr_name = f"mark{int(single_choice)}"
				if hasattr(quiz_doc, mark_attr_name):
					marks = getattr(quiz_doc, mark_attr_name)
					response_marks.append(marks)  # Append marks for this choice
					fund_response.append("response", {
							"id": quiz_id,
							"choices": str(single_choice),
							"marks": marks
						})
				else:
					raise AttributeError(f"'{quiz_id}' object has no attribute '{mark_attr_name}'")
			elif multi_choice is not None:
				if isinstance(multi_choice, list):
					for choice in multi_choice:
						mark_attr_name = f"mark_{int(choice)}"
						if hasattr(quiz_doc, mark_attr_name):
							marks = getattr(quiz_doc, mark_attr_name)
							response_marks.append(marks)  # Append marks for this choice
							fund_response.append("response", {
								"id": quiz_id,
								"choices": str(choice),
								"marks": marks
							})
						else:
							raise AttributeError(f"'{quiz_id}' object has no attribute '{mark_attr_name}'")
				else:
					mark_attr_name = f"mark_{int(multi_choice)}"
					if hasattr(quiz_doc, mark_attr_name):
						marks = getattr(quiz_doc, mark_attr_name)
						response_marks.append(marks)
						fund_response.append("response", {
							"id": quiz_id,
							"choices": str(multi_choice),
							"marks": marks 
						})
					else:
						raise AttributeError(f"'{quiz_id}' object has no attribute '{mark_attr_name}'")
			
		fund_response.insert(ignore_permissions=True)
		frappe.db.commit()  
		# Calculate total marks
		total_marks = sum(response_marks)
		return {"status": True, "message": "Responses created successfully", "total": total_marks}
	except Exception as e:
		return {"status": False, "message": str(e)}
