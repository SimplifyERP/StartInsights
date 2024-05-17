import frappe
import html2text
import json

@frappe.whitelist()
def get_fundability_quiz(user_id,customer_group,question_id,option,attempt_status,type_of_question,fundability_quiz_response_id,quiz_completed):
    if not option == "":
        if type_of_question == "Single":
            deocde_list = [int(option)]
        elif type_of_question == "MultiSelect":
            deocde_list = [int(x) for x in option.split(',') if x]
    fundability = []
    status = False
    message = ""
    option_map = {
        0:"Any Option",
        1:"First Option",
        2:"Second Option",
        3:"Third Option",
        4:"Fourth Option",
        5:"Fifth Option",
        6:"Sixth Option"    
    }
    try:
        get_quiz = frappe.db.get_value("SI Quiz Flow",{"disabled":0,"customer_group":customer_group},["name"])
        quiz_list = []
        if not (question_id and option == None) and type_of_question == "" :
            quiz_flow_table = frappe.db.get_all("SI Quiz Flow Table",{"parent":get_quiz},["*"],order_by='idx ASC',limit=1)
            for quiz in quiz_flow_table:
                options_dict = [
                    {
                        "option": quiz.option_1 or "",
                    },
                    {
                        "option": quiz.option_2 or "",
                    },
                    {
                        "option": quiz.option_3 or "",
                    },
                    {
                        "option": quiz.option_4 or "",
                    },
                    {
                        "option": quiz.option_5 or "",
                    },
                    {
                        "option": quiz.option_6 or "",
                    }
                ]
                quiz_question_remove_html = html2text.html2text(quiz.question_name or "").strip()
                get_type_of_question = frappe.get_doc("SI Quiz",quiz.fundability_quiz_question)
                quiz_details = {
                    "id":get_quiz, 
                    "type_of_question":get_type_of_question.type,
                    "question_id":quiz.fundability_quiz_question,
                    "question_name":quiz_question_remove_html,
                    "options": options_dict,      
                }
                quiz_list.append(quiz_details)
                status = True
                message = "Success"
        else:
            if type_of_question == "Single" and len(deocde_list) == 1:
                quiz_flow_table = frappe.db.get_value("SI Quiz Flow Table",{"parent":get_quiz,"fundability_quiz_question":question_id},["select_option"])
                if quiz_flow_table == option_map.get(0):
                    next_question = frappe.db.get_value("SI Quiz Flow Table",{"parent":get_quiz,"fundability_quiz_question":question_id},["next_display_question_no"])
                else:
                    next_question = frappe.db.get_value("SI Quiz Flow Table",{"parent":get_quiz,"fundability_quiz_question":question_id,"select_option":option_map.get(deocde_list[0])},["next_display_question_no"])   
            elif type_of_question == "MultiSelect":
                next_question = frappe.db.get_value("SI Quiz Flow Table",{"parent":get_quiz,"fundability_quiz_question":question_id,"select_option":option_map.get(0)},["next_display_question_no"])
              
            if next_question:
                get_question_and_options = frappe.get_doc("SI Quiz",next_question)
                quiz_question_remove_html = html2text.html2text(get_question_and_options.question or "").strip()
                options_dict = [
                    {
                        "option": get_question_and_options.option_1 or "",
                    },
                    {
                        "option": get_question_and_options.option_2 or "",
                    },
                    {
                        "option": get_question_and_options.option_3 or "",
                    },
                    {
                        "option": get_question_and_options.option_4 or "",
                    },
                    {
                        "option": get_question_and_options.option_5 or "",
                    },
                    {
                        "option": get_question_and_options.option_6 or "",
                    }
                ]
                quiz_details = {
                    "id":get_quiz, 
                    "type_of_question":get_question_and_options.type,
                    "question_id":get_question_and_options.name,
                    "question_name":quiz_question_remove_html,
                    "options": options_dict,                 
                }
                quiz_list.append(quiz_details)
                fundability = mark_fundability_quiz(user_id,customer_group,question_id,option,attempt_status,type_of_question,fundability_quiz_response_id)
                # get_total_marks(quiz_completed,fundability_quiz_response_id)
                status = True
                message = "Success"
            else:
                status = False
                message = "Selected Option has not Question"    
        return {"status":status,"message":message,"quiz_id_count":(get_quiz_question_count(customer_group)),"fundability_details":quiz_list,"fundability_id":fundability or ""}
    except Exception as e:
        return {"status":False,"message":e}	

def get_quiz_question_count(customer_group):
    get_quiz = frappe.db.get_value("SI Quiz Flow", {"disabled": 0, "customer_group": customer_group}, ["name"])
    get_quiz_question_flow = frappe.db.get_all("SI Quiz Flow Table", {"parent": get_quiz}, ["fundability_quiz_question"])
    seen = set()
    unique_quiz_question_flow = []
    for quiz_question in get_quiz_question_flow:
        quiz_question_id = quiz_question["fundability_quiz_question"]
        if quiz_question_id not in seen:
            unique_quiz_question_flow.append(quiz_question)
            seen.add(quiz_question_id)
    return len(unique_quiz_question_flow)


def mark_fundability_quiz(user_id,customer_group,question_id,option,attempt_status,type_of_question,fundability_quiz_response_id):
    if not option == "":
        if type_of_question == "Single":
            deocde_list = [int(option)]
        elif type_of_question == "MultiSelect":
            deocde_list = [int(x) for x in option.split(',') if x]
    if type_of_question == "Single" and len(deocde_list) == 1: 
        if deocde_list[0] == 1:
            get_quiz_mark = frappe.db.get_value("SI Quiz",{"name":question_id},["option_1","mark_1"])
        elif deocde_list[0] == 2:
            get_quiz_mark = frappe.db.get_value("SI Quiz",{"name":question_id},["option_2","mark_2"])
        elif deocde_list[0] == 3:
            get_quiz_mark = frappe.db.get_value("SI Quiz",{"name":question_id},["option_3","mark_3"])        
        elif deocde_list[0] == 4:
            get_quiz_mark = frappe.db.get_value("SI Quiz",{"name":question_id},["option_4","mark_4"])
        elif deocde_list[0] == 5:
            get_quiz_mark = frappe.db.get_value("SI Quiz",{"name":question_id},["option_5","mark_5"])
        elif deocde_list[0] == 6:
            get_quiz_mark = frappe.db.get_value("SI Quiz",{"name":question_id},["option_6","mark_6"])    
        else:
            get_quiz_mark = 0
         
        if int(attempt_status) == 1:
            new_quiz_response = frappe.new_doc("SI Quiz User Response")
            new_quiz_response.user = user_id
            new_quiz_response.customer_group = customer_group
            response_dict = {
                "question_id": question_id,
                "user_response_option": deocde_list[0],
                "marks": get_quiz_mark[1]
            }
            if deocde_list[0] == 1:
                response_dict["option_1"] = get_quiz_mark[0]
            elif deocde_list[0] == 2:
                response_dict["option_2"] = get_quiz_mark[0]
            elif deocde_list[0] == 3:
                response_dict["option_3"] = get_quiz_mark[0]
            elif deocde_list[0] == 4:
                response_dict["option_4"] = get_quiz_mark[0]
            elif deocde_list[0] == 5:
                response_dict["option_4"] = get_quiz_mark[0]
            elif deocde_list[0] == 6:
                response_dict["option_6"] = get_quiz_mark[0]

            new_quiz_response.append("response", response_dict)
            new_quiz_response.save(ignore_permissions=True) 
            frappe.db.commit()
            return new_quiz_response.name
        else:
            if frappe.db.exists("SI Quiz User Response",{"name":fundability_quiz_response_id}):
                update_quiz_response = frappe.get_doc("SI Quiz User Response",fundability_quiz_response_id)
                response_dict = {
                    "question_id": question_id,
                    "user_response_option": option[0],
                    "marks": get_quiz_mark[1]
                }
                if deocde_list[0] == 1:
                    response_dict["option_1"] = get_quiz_mark[0]
                elif deocde_list[0] == 2:
                    response_dict["option_2"] = get_quiz_mark[0]
                elif deocde_list[0] == 3:
                    response_dict["option_3"] = get_quiz_mark[0]
                elif deocde_list[0] == 4:
                    response_dict["option_4"] = get_quiz_mark[0]
                elif deocde_list[0] == 5:
                    response_dict["option_4"] = get_quiz_mark[0]
                elif deocde_list[0] == 6:
                    response_dict["option_6"] = get_quiz_mark[0]

                update_quiz_response.append("response", response_dict)
                update_quiz_response.save(ignore_permissions=True)
                frappe.db.commit()
                return fundability_quiz_response_id

    elif type_of_question == "MultiSelect":
        response_list = []
        total_mark = 0
        for options in deocde_list:
            if options == 1:
                marks = frappe.db.get_value("SI Quiz", {"name": question_id}, ["option_1", "mark_1"])
                total_mark += marks[1] if marks else 0
            elif options == 2:
                marks = frappe.db.get_value("SI Quiz", {"name": question_id}, ["option_2", "mark_2"])
                total_mark += marks[1] if marks else 0
            elif options == 3:
                marks = frappe.db.get_value("SI Quiz", {"name": question_id}, ["option_3", "mark_3"]) 
                total_mark += marks[1] if marks else 0
            elif options == 4:
                marks = frappe.db.get_value("SI Quiz", {"name": question_id}, ["option_4", "mark_4"])
                total_mark += marks[1] if marks else 0
            elif options == 5:
                marks = frappe.db.get_value("SI Quiz", {"name": question_id}, ["option_5", "mark_5"])
                total_mark += marks[1] if marks else 0
            elif options == 6:
                marks = frappe.db.get_value("SI Quiz", {"name": question_id}, ["option_6", "mark_6"])
                total_mark += marks[1] if marks else 0
            else:
                total_mark += 0 

            if int(attempt_status) == 1:
                new_quiz_response = frappe.new_doc("SI Quiz User Response")
                new_quiz_response.user = user_id
                new_quiz_response.customer_group = customer_group
                
                for selected_option in deocde_list:
                    option_text = frappe.db.get_value("SI Quiz", {"name": question_id}, "option_" + str(selected_option))
                    mark = frappe.db.get_value("SI Quiz", {"name": question_id}, "mark_" + str(selected_option))
                    response_dict = {
                        "question_id": question_id,
                        "user_response_option": selected_option,
                        "option_" + str(selected_option) : option_text,
                        "marks": mark if mark else 0
                    }
                    response_list.append(response_dict)
                new_quiz_response.extend("response", response_list)
                new_quiz_response.save(ignore_permissions=True)
                frappe.db.commit()
                return new_quiz_response.name
            else:
                if frappe.db.exists("SI Quiz User Response",{"name":fundability_quiz_response_id}):
                    update_quiz_response = frappe.get_doc("SI Quiz User Response",fundability_quiz_response_id)
                    for selected_option in deocde_list:
                        option_text = frappe.db.get_value("SI Quiz", {"name": question_id}, "option_" + str(selected_option))
                        mark = frappe.db.get_value("SI Quiz", {"name": question_id}, "mark_" + str(selected_option))
                        response_dict = {
                            "question_id": question_id,
                            "user_response_option": selected_option,
                            "option_" + str(selected_option) : option_text,
                            "marks": mark if mark else 0
                        }
                        response_list.append(response_dict)
                    update_quiz_response.extend("response", response_list)
                    update_quiz_response.save(ignore_permissions=True)
                    frappe.db.commit()
                    return fundability_quiz_response_id


def get_total_marks(quiz_completed,fundability_quiz_response_id):
    if quiz_completed == "True":
        total_marks = frappe.db.sql("""
            SELECT SUM(fs.marks) AS total_marks 
            FROM `tabSI Quiz User Response` si  
            LEFT JOIN `tabQuiz Response` fs ON si.name = fs.parent 
            WHERE si.name = %s
        """, (fundability_quiz_response_id), as_dict=True)[0]

        frappe.db.set_value("SI Quiz User Response",fundability_quiz_response_id,"total_quiz_marks",total_marks["total_marks"])
        return type(total_marks["total_marks"])
   

            