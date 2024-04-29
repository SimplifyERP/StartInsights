import frappe
import html2text

@frappe.whitelist()
def get_fundability_quiz(customer_group,question_id,option):
    status = False
    message = ""
    option_map = {
        0:"All Option",
        1:"First Option",
        2:"Second Option",
        3:"Third Option",
        4:"Fourth Option",
        5:"Fifth Option",
        6:"Sixth Option"    
    }
    try:
        get_quiz = frappe.db.get_value("Fundability Quiz Flow",{"disabled":0,"customer_group":customer_group},["name"])
        quiz_list = []
        if not question_id and option == "":
            quiz_flow_table = frappe.db.get_all("Fundability Quiz Flow Table",{"parent":get_quiz},["*"],order_by='idx ASC',limit=1)
            for quiz in quiz_flow_table:
                quiz_question_remove_html = html2text.html2text(quiz.question_name or "").strip()
                get_type_of_question = frappe.get_doc("Fundability Quiz",quiz.fundability_quiz_question)
                quiz_details = {
                    "id":get_quiz, 
                    "type_of_question":get_type_of_question.type,
                    "question_id":quiz.fundability_quiz_question,
                    "question_name":quiz_question_remove_html,
                    "option_1":quiz.option_1 or "",
                    "option_2":quiz.option_2 or "",
                    "option_3":quiz.option_3 or "",
                    "option_4":quiz.option_4 or "",
                    "option_5":quiz.option_5 or "",
                    "option_6":quiz.option_6 or "",           
                }
                quiz_list.append(quiz_details)
                status = True
                message = "Success"
        else:
            quiz_flow_table = frappe.db.get_value("Fundability Quiz Flow Table",{"parent":get_quiz,"fundability_quiz_question":question_id,"select_option":option_map.get(option)},["next_display_question_no"])
            if quiz_flow_table:
                get_question_and_options = frappe.get_doc("Fundability Quiz",quiz_flow_table)
                quiz_question_remove_html = html2text.html2text(get_question_and_options.question or "").strip()
                quiz_details = {
                    "id":get_quiz, 
                    "type_of_question":get_question_and_options.type,
                    "question_id":get_question_and_options.name,
                    "question_name":quiz_question_remove_html,
                    "option_1":get_question_and_options.option_1 or "",
                    "option_2":get_question_and_options.option_2 or "",
                    "option_3":get_question_and_options.option_3 or "",
                    "option_4":get_question_and_options.option_4 or "",
                    "option_5":get_question_and_options.option_5 or "",
                    "option_6":get_question_and_options.option_6 or "",           
                }
                quiz_list.append(quiz_details)
                status = True
                message = "Success"
            else:
                status = False
                message = "Wrong Option or Wrong Question ID"    
        return {"status":status,"message":message,"fundability_details":quiz_list}
    except Exception as e:
        return {"status":False,"message":e}	