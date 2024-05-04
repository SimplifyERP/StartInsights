import frappe
import html2text

@frappe.whitelist()
def get_fundability_quiz(user_id,customer_group,question_id,option,attempt_status,fundability_quiz_response_id):
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
        quiz_response = mark_fundability_quiz(user_id,customer_group,question_id,option,attempt_status,fundability_quiz_response_id)      
        return {"status":status,"message":message,"fundability_details":quiz_list,"fundability_quiz_response_id":quiz_response}
    except Exception as e:
        return {"status":False,"message":e}	
    
def mark_fundability_quiz(user_id,customer_group,question_id,option,attempt_status,fundability_quiz_response_id):
    # if option == 1:
    #     get_quiz_mark = frappe.db.get_value("Fundability Quiz",{"name":question_id},["mark_1"])
    # elif option == 2:
    #     get_quiz_mark = frappe.db.get_value("Fundability Quiz",{"name":question_id},["mark_2"])
    # elif option == 3:
    #     get_quiz_mark = frappe.db.get_value("Fundability Quiz",{"name":question_id},["mark_3"])        
    # elif option == 4:
    #     get_quiz_mark = frappe.db.get_value("Fundability Quiz",{"name":question_id},["mark_4"])
    # elif option == 5:
    #     get_quiz_mark = frappe.db.get_value("Fundability Quiz",{"name":question_id},["mark_5"])
    # elif option == 6:
    #     get_quiz_mark = frappe.db.get_value("Fundability Quiz",{"name":question_id},["mark_6"])    
    # else:
    #     get_quiz_mark = "No Option in Backend"
    # return get_quiz_mark    

    if not frappe.db.exists("Fundability Quiz User Response",{"user":user_id}):
        quiz = "test"
        # new_quiz_response = frappe.new_doc("Fundability Quiz User Response")
        # new_quiz_response.user = user_id
        # new_quiz_response.attempt_status = 1
        # new_quiz_response.customer_group = customer_group
        # new_quiz_response.save(ignore_permissions=True) 
        # frappe.db.commit() 
    else:
        if attempt_status == 1:
            quiz = "no"
            # new_quiz_response = frappe.new_doc("Fundability Quiz User Response")
            # new_quiz_response.user = user_id
            # new_quiz_response.attempt_status = 1
            # new_quiz_response.customer_group = customer_group
            # new_quiz_response.save(ignore_permissions=True) 
            # frappe.db.commit()
        else: 
            quiz = "yes"
            # update_quiz_response = frappe.get_doc("Fundability Quiz Response",fundability_quiz_response_id)
            # update_quiz_response.customer_group = "Investors"
            # update_quiz_response.save(ignore_permissions=True)
            # frappe.db.commit()
    return quiz      
    #     return {"status":True,"message":get_quiz_mark}
    # except Exception as e:
    #     return {"status":False,"message":e}