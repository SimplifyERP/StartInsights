import frappe


#create and get the data of quiz question and options
@frappe.whitelist()
def create_i_frame_quiz(user_id,question_id,option,attempt_status,type_of_question,quiz_response_id,quiz_completed):
    if not option == "":
        if type_of_question == "Single":
            deocde_list = [int(option)]
        elif type_of_question == "MultiSelect":
            deocde_list = [int(x) for x in option.split(',') if x]
    quiz_response = []  
    score = []    
    quiz_count = []  
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
        get_quiz = frappe.db.get_value("Quiz Flow",{"disabled":0,"quiz_group":"Startups"},["name"])
        quiz_list = []
        if not (question_id and option == None) and type_of_question == "" :
            quiz_flow_table = frappe.db.get_all("Quiz Flow Table",{"parent":get_quiz},["*"],order_by='idx ASC',limit=1)
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
                get_type_of_question = frappe.get_doc("Quiz",quiz.quiz_question_id)
                quiz_details = {
                    "question_id":quiz.quiz_question_id,
                    "id":get_quiz,
                    "type_of_question":get_type_of_question.quiz_type,
                    "question_name":get_type_of_question.quiz_question,
                    "options": options_dict,      
                }
                quiz_list.append(quiz_details)
        else:
            if type_of_question == "Single" and len(deocde_list) == 1:       
                quiz_flow_table = frappe.db.get_value("Quiz Flow Table",{"parent":get_quiz,"quiz_question_id":question_id},["select_option"]) 
                if quiz_flow_table == option_map.get(0):
                    next_question = frappe.db.get_value("Quiz Flow Table",{"parent":get_quiz,"quiz_question_id":question_id},["next_quiz_question_id"])
                else:
                    next_question = frappe.db.get_value("Quiz Flow Table",{"parent":get_quiz,"quiz_question_id":question_id,"select_option":option_map.get(deocde_list[0])},["next_quiz_question_id"])   
            elif type_of_question == "MultiSelect":
                next_question = frappe.db.get_value("Quiz Flow Table",{"parent":get_quiz,"quiz_question_id":question_id,"select_option":option_map.get(0)},["next_quiz_question_id"])
            if next_question:
                get_question_and_options = frappe.get_doc("Quiz",next_question)   
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
                    "question_id":get_question_and_options.name,
                    "id":get_quiz, 
                    "type_of_question":get_question_and_options.quiz_type, 
                    "question_name":get_question_and_options.quiz_question,
                    "options": options_dict,                  
                }
                quiz_list.append(quiz_details) 
                quiz_response = create_quiz_user_response(question_id,option,attempt_status,type_of_question,quiz_response_id)
                quiz_count = get_quiz_count()
            else:
                if quiz_completed == 1:
                    quiz_response = create_quiz_user_response(question_id,option,attempt_status,type_of_question,quiz_response_id)
                    get_total_score(quiz_completed,quiz_response_id)
                    quiz_count = [] 
                    quiz_list = [] 
                    score = []


        return {"status":True,"message":"Sucessfully Completed QUIZ","user_status":get_quiz_user_status(user_id),"quiz_id_count":quiz_count,"fundability_details":quiz_list,"fundability_id":quiz_response,"score":score or []}
    except Exception as e:
        return {"status":False,"message":e}

#get the quiz count of how many quiz questions enter in quiz flow doctype
def get_quiz_count():
    get_quiz = frappe.db.get_value("Quiz Flow", {"disabled": 0, "quiz_group": "Startups"},["name"])
    get_quiz_question_flow = frappe.db.get_all("Quiz Flow Table",{"parent": get_quiz},["quiz_question_id"])
    seen = set()
    unique_quiz_question_flow = []
    for quiz_question in get_quiz_question_flow:
        quiz_question_id = quiz_question["quiz_question_id"]
        if quiz_question_id not in seen:
            unique_quiz_question_flow.append(quiz_question)
            seen.add(quiz_question_id)
    return len(unique_quiz_question_flow)

def create_quiz_user_response(question_id,option,attempt_status,type_of_question,quiz_response_id):
    if not option == "":
        if type_of_question == "Single":
            deocde_list = [int(option)]
        elif type_of_question == "MultiSelect":
            deocde_list = [int(x) for x in option.split(',') if x]
    #checking the which option will match the data
    if type_of_question == "Single" and len(deocde_list) == 1: 
        if deocde_list[0] == 1:
            get_quiz_mark = frappe.db.get_value("Quiz",{"name":question_id},["option_1","mark_1"])
        elif deocde_list[0] == 2:
            get_quiz_mark = frappe.db.get_value("Quiz",{"name":question_id},["option_2","mark_2"])
        elif deocde_list[0] == 3:
            get_quiz_mark = frappe.db.get_value("Quiz",{"name":question_id},["option_3","mark_3"])        
        elif deocde_list[0] == 4:
            get_quiz_mark = frappe.db.get_value("Quiz",{"name":question_id},["option_4","mark_4"])
        elif deocde_list[0] == 5:
            get_quiz_mark = frappe.db.get_value("Quiz",{"name":question_id},["option_5","mark_5"])
        elif deocde_list[0] == 6:
            get_quiz_mark = frappe.db.get_value("Quiz",{"name":question_id},["option_6","mark_6"])    
        else:
            get_quiz_mark = 0        

        if int(attempt_status) == 1:
            new_quiz_response = frappe.new_doc("Quiz User Response")
            new_quiz_response.quiz_group = "Startups"
            response_dict = {
                "quiz_question_id": question_id,
                "response_option": deocde_list[0],
                "response_marks": get_quiz_mark[1]
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

            new_quiz_response.append("response_table", response_dict)
            new_quiz_response.save(ignore_permissions=True) 
            frappe.db.commit()
            return new_quiz_response.name  
        else:
            get_quiz_completed = frappe.db.get_value("Quiz User Response",{"name":quiz_response_id},["quiz_completed_status"])
            if get_quiz_completed == 0:
                if frappe.db.exists("Quiz User Response",{"name":quiz_response_id}):
                    update_quiz_response = frappe.get_doc("Quiz User Response",quiz_response_id)  
                    update_quiz_response.quiz_completed_status = 1   
                    response_dict = {
                        "quiz_question_id": question_id,
                        "response_option": option[0],
                        "response_marks": get_quiz_mark[1]
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

                    update_quiz_response.append("response_table", response_dict)
                    update_quiz_response.save(ignore_permissions=True)
                    frappe.db.commit()
                    return quiz_response_id
            else:
                return quiz_response_id    
                
    elif type_of_question == "MultiSelect":
        response_list = []
        total_mark = 0
        for options in deocde_list:
            if options == 1:
                marks = frappe.db.get_value("Quiz", {"name": question_id}, ["option_1", "mark_1"])
                total_mark += marks[1] if marks else 0
            elif options == 2:
                marks = frappe.db.get_value("Quiz", {"name": question_id}, ["option_2", "mark_2"])
                total_mark += marks[1] if marks else 0
            elif options == 3:
                marks = frappe.db.get_value("Quiz", {"name": question_id}, ["option_3", "mark_3"]) 
                total_mark += marks[1] if marks else 0
            elif options == 4:
                marks = frappe.db.get_value("Quiz", {"name": question_id}, ["option_4", "mark_4"])
                total_mark += marks[1] if marks else 0
            elif options == 5:
                marks = frappe.db.get_value("Quiz", {"name": question_id}, ["option_5", "mark_5"])
                total_mark += marks[1] if marks else 0
            elif options == 6:
                marks = frappe.db.get_value("Quiz", {"name": question_id}, ["option_6", "mark_6"])
                total_mark += marks[1] if marks else 0
            else:
                total_mark += 0 

            if int(attempt_status) == 1:
                new_quiz_response = frappe.new_doc("Quiz User Response")
                new_quiz_response.quiz_group = "Startups"
                
                for selected_option in deocde_list:
                    option_text = frappe.db.get_value("Quiz", {"name": question_id}, "option_" + str(selected_option))
                    mark = frappe.db.get_value("Quiz", {"name": question_id}, "mark_" + str(selected_option))
                    response_dict = {
                        "quiz_question_id": question_id,
                        "response_option": selected_option,
                        "option_" + str(selected_option) : option_text,
                        "response_marks": mark if mark else 0
                    }
                    response_list.append(response_dict)
                new_quiz_response.extend("response_table", response_list)
                new_quiz_response.save(ignore_permissions=True)
                frappe.db.commit()
                return new_quiz_response.name
            else:
                get_quiz_completed = frappe.db.get_value("Quiz User Response",{"name":quiz_response_id},["quiz_completed_status"])
                if get_quiz_completed == 0:
                    if frappe.db.exists("Quiz User Response",{"name":quiz_response_id}):
                        update_quiz_response = frappe.get_doc("Quiz User Response",quiz_response_id)
                        update_quiz_response.quiz_completed_status = 1
                        for selected_option in deocde_list:
                            option_text = frappe.db.get_value("Quiz", {"name": question_id}, "option_" + str(selected_option))
                            mark = frappe.db.get_value("Quiz", {"name": question_id}, "mark_" + str(selected_option))
                            response_dict = {
                                "quiz_question_id": question_id,
                                "response_option": selected_option,
                                "option_" + str(selected_option) : option_text,
                                "response_marks": mark if mark else 0
                            }
                            response_list.append(response_dict)
                        update_quiz_response.extend("response_table", response_list)
                        update_quiz_response.save(ignore_permissions=True)
                        frappe.db.commit()
                        return quiz_response_id
                else:
                    return quiz_response_id        


def get_total_score(quiz_completed,quiz_response_id):
    score_card_list = []
    if quiz_completed == 1:
        total_marks = frappe.db.sql("""
            SELECT SUM(fs.response_marks) AS total_marks,si.score_review_statement as review_statement
            FROM `tabQuiz User Response` si  
            LEFT JOIN `tabUser Response Table` fs ON si.name = fs.parent 
            WHERE si.name = %s
        """, (quiz_response_id), as_dict=True)[0]

        frappe.db.set_value("Quiz User Response",quiz_response_id,"total_score",total_marks["total_marks"])
        score_card = {
            "score":total_marks["total_marks"],
            "review":total_marks["review_statement"]
        }
        score_card_list.append(score_card)
        return score_card_list

def get_quiz_user_status(user_id):
    user_status = 0
    get_quiz_user = frappe.db.get_value("Quiz Lead",{"name":user_id},["name"])
    if get_quiz_user:
        user_status = True
    else:
        user_status = False
    return user_status        

@frappe.whitelist()
def get_quiz_score(quiz_response_id,user_id,first_name,last_name,company,password):
    try:
        score_card_list = []
        if not frappe.db.exists("Quiz Lead",user_id):
            new_quiz_form = frappe.new_doc("Quiz Lead")
            new_quiz_form.first_name = first_name
            new_quiz_form.last_name = last_name
            new_quiz_form.full_name = first_name + " " + last_name
            new_quiz_form.user_id = user_id
            new_quiz_form.email_id = user_id
            new_quiz_form.password = password
            new_quiz_form.company = company
            new_quiz_form.save(ignore_permissions=True)
            frappe.db.commit()
            
            get_quiz_lead_details = frappe.get_doc("Quiz Lead",new_quiz_form.name)

            get_score = frappe.get_doc("Quiz User Response",quiz_response_id)
            get_score.user_id = get_quiz_lead_details.name
            get_score.full_name = get_quiz_lead_details.full_name
            get_score.company = get_quiz_lead_details.company
            get_score.save(ignore_permissions=True)
            frappe.db.commit()

            score_card = {
                "score":get_score.total_score,
                "review":get_score.score_review_statement
            }
            score_card_list.append(score_card)
        return {"status":True,"score_card":score_card_list}    
    except Exception as e:
        return {"status":False,"message":e}

@frappe.whitelist()
def get_score_as_login(user_id,password,quiz_response_id):
    try:
        score_card_list = []
        get_quiz_lead = frappe.db.get_value("Quiz Lead",{"name":user_id},["password"])
        if get_quiz_lead == password:
            get_quiz_lead_details = frappe.get_doc("Quiz Lead",user_id)

            get_score = frappe.get_doc("Quiz User Response",quiz_response_id)
            get_score.user_id = get_quiz_lead_details.name
            get_score.full_name = get_quiz_lead_details.full_name
            get_score.company = get_quiz_lead_details.company
            get_score.save(ignore_permissions=True)
            frappe.db.commit()

            score_card = {
                "score":get_score.total_score,
                "review":get_score.score_review_statement
            }
            score_card_list.append(score_card)
        return {"status":True,"score_card":score_card_list}
    except Exception as e:
        return {"status":False}