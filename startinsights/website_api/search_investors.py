import frappe
from startinsights.custom import get_domain_name


@frappe.whitelist()
def get_search_investors_list(page_no,funding_stage,user_id):
    search_investors = []
    image_url = ""
    favourites_status = False
    fund_rasing = []
    try:
        funding_stages_tuple = tuple(funding_stage)
        investors_count = frappe.db.count("Search Investors",{"disabled":0})
        page_no_calulate = calculate_count(page_no)
        if not funding_stage == []:
            search_investors_list = frappe.db.sql(""" SELECT * FROM `tabSearch Investors` ORDER BY name ASC LIMIT %s OFFSET %s """, (page_no_calulate[1], page_no_calulate[0]), as_dict=True)
        else:
            search_investors_list = frappe.db.sql(""" SELECT si.* FROM `tabSearch Investors` si  LEFT JOIN `tabInvestor Funding Stages` fs ON si.name = fs.parent 
                            WHERE fs.funding_stages IN %s ORDER BY name ASC LIMIT %s OFFSET %s """, (funding_stages_tuple,page_no_calulate[1], page_no_calulate[0]), as_dict=True)
        for investors_details in search_investors_list: 
            favourite_investor = frappe.db.get_value("Search Investors Favourites",{"user_id":user_id,"investors":investors_details.name},['favourites_status'])
            if favourite_investor == 1:
                favourites_status = True
            else:
                favourites_status = False    

            if investors_details.investor_logo:
                image_url = get_domain_name() + investors_details.get('investor_logo')
            else:
                image_url = ""    
            fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':investors_details.name},['funding_stages'])

            investors_list = {
                "id":investors_details.name,
                "name":investors_details.name,
                "favourites_status":favourites_status,
                "title":investors_details.investor_title or "",
                "logo":image_url,
                "investor_verified":investors_details.investor_verified or "",
                "linkedin":investors_details.investor_linkedin or "",
                "website":investors_details.investor_website or "",
                "about_us":investors_details.about_us or "",
                "value_add":investors_details.value_add or "",
                "firm_type":investors_details.firm_type or "",
                "hq":investors_details.hq or "",
                "funding_requirements":investors_details.funding_requirements or "",
                "funding_stages_table":fund_rasing,          
                "min_check_size":investors_details.min_check_size or "0",
                "max_check_size":investors_details.max_check_size or "0"
            }
            search_investors.append(investors_list) 
        return {"status":True,"investors_count":investors_count,"search_investors_list":search_investors}
    except Exception as e:
        return {"status":False,"message":e}
    
# calculate the page count of given data
def calculate_count(page_count):
    if int(page_count) <= 0:
        return None, None  # Handle invalid page counts
    # Calculate min and max counts
    min_count = (int(page_count) - 1) * 8
    max_count = min_count + 8
    return min_count, max_count

@frappe.whitelist()
def set_investors_favourites(user_id,investor_id):
    status = ""
    message = ""
    try:
        if not frappe.db.exists("Search Investors Favourites",{'user_id':user_id,'investors':investor_id}):
            new_favourite_investor = frappe.new_doc("Search Investors Favourites")
            new_favourite_investor.user_id = user_id
            new_favourite_investor.investors = investor_id
            new_favourite_investor.favourites_status = 1
            new_favourite_investor.save(ignore_permissions=True)
            frappe.db.commit()

            #Updating the recommended investors count in search investors master
            get_search_investors = frappe.get_doc("Search Investors",investor_id)
            get_search_investors.recommended_investors_count = get_search_investors.recommended_investors_count + 1
            get_search_investors.save(ignore_permissions=True)
            frappe.db.commit()

            status = True
            message = "Investor Favourite Created"
        else:
            get_favourites = frappe.db.get_value("Search Investors Favourites",{'user_id':user_id,'investors':investor_id},['name'])
            update_favourites = frappe.get_doc("Search Investors Favourites",get_favourites)
            update_favourites.favourites_status = 1
            update_favourites.save(ignore_permissions=True)
            frappe.db.commit()

            status = True
            message = "Investor Favourite Updated"
        return {"status":status,"message":message}    
    except Exception as e:
        return {"status":False,"message":e}


@frappe.whitelist()
def get_favourite_investors(user_id,status,page_no):
    fund_rasing = []
    try:
        search_investors_list = []
        page_no_calulate = calculate_count(page_no)
        favourite_investors_list = frappe.db.sql(""" SELECT investors FROM `tabSearch Investors Favourites` WHERE user_id = %s AND favourites_status = %s  ORDER BY name ASC LIMIT %s OFFSET %s """, (user_id,status,page_no_calulate[1], page_no_calulate[0]), as_dict=True)
        for favourite in favourite_investors_list:
            get_search_investors_list = frappe.get_doc("Search Investors",favourite.investors)
            if get_search_investors_list.investor_logo:
                image_url = get_domain_name() + get_search_investors_list.get('investor_logo')
            else:
                image_url = ""    
            fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':get_search_investors_list.name},['funding_stages'])
            investors_list = {
                "id":get_search_investors_list.name,
                "name":get_search_investors_list.name,
                "favourites_status":True,
                "title":get_search_investors_list.investor_title or "",
                "logo":image_url,
                "investor_verified":get_search_investors_list.investor_verified or "",
                "linkedin":get_search_investors_list.investor_linkedin or "",
                "website":get_search_investors_list.investor_website or "",
                "about_us":get_search_investors_list.about_us or "",
                "value_add":get_search_investors_list.value_add or "",
                "firm_type":get_search_investors_list.firm_type or "",
                "hq":get_search_investors_list.hq or "",
                "funding_requirements":get_search_investors_list.funding_requirements or "",
                "funding_stages_table":fund_rasing,          
                "min_check_size":get_search_investors_list.min_check_size or "0",
                "max_check_size":get_search_investors_list.max_check_size or "0"
            }
            search_investors_list.append(investors_list)
        return {"status":True,"search_investors_list":search_investors_list}
    except Exception as e:
        return {"status":False,"message":e}

@frappe.whitelist()
def remove_favourites_investors(user_id,investor_id,status):
    try:
        get_favourite = frappe.db.get_value("Search Investors Favourites",{'user_id':user_id,'investors':investor_id},['name'])
        frappe.db.set_value("Search Investors Favourites",get_favourite,"favourites_status",status)
        return {"status":True,"favourite_status":"favourite removed"}
    except Exception as e:
        return {"status":False,"message":e}


@frappe.whitelist()
def get_recommended_search_investors():
    search_investors = []
    fund_rasing = []
    try:
        search_investors_list = frappe.db.sql(""" SELECT * FROM `tabSearch Investors` WHERE recommended_investors_count > 0  ORDER BY recommended_investors_count DESC LIMIT 4 """,as_dict=1)
        for investors_details in search_investors_list:
            if investors_details.investor_logo:
                image_url = get_domain_name() + investors_details.get('investor_logo')
            else:
                image_url = ""    
            fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':investors_details.name},['funding_stages'])

            investors_list = {
                "id":investors_details.name,
                "name":investors_details.name,
                "title":investors_details.investor_title or "",
                "logo":image_url,
                "investor_verified":investors_details.investor_verified or "",
                "linkedin":investors_details.investor_linkedin or "",
                "website":investors_details.investor_website or "",
                "about_us":investors_details.about_us or "",
                "value_add":investors_details.value_add or "",
                "firm_type":investors_details.firm_type or "",
                "hq":investors_details.hq or "",
                "funding_requirements":investors_details.funding_requirements or "",
                "funding_stages_table":fund_rasing,          
                "min_check_size":investors_details.min_check_size or "0",
                "max_check_size":investors_details.max_check_size or "0"
            }
            search_investors.append(investors_list) 
        return {"status":True,"message":search_investors}
    except Exception as e:
        return {"status":False,"message":e}
    

@frappe.whitelist()
def get_search_investors_serach_bar(page_no,funding_stage,search_key,user_id):
    try:
        search_bar_investors_list = []
        funding_stages_tuple = tuple(funding_stage)
        investors_count = frappe.db.sql(""" SELECT count(name) as investor_counts FROM `tabSearch Investors` WHERE investor_title LIKE %s  """,('%'+search_key+'%'),as_dict=True)
        page_no_calulate = calculate_count(page_no)
        if funding_stage == []:
            search_investors_list = frappe.db.sql(""" SELECT * FROM `tabSearch Investors` WHERE investor_title LIKE %s  ORDER BY name ASC LIMIT %s OFFSET %s """,('%'+search_key+'%',page_no_calulate[1],page_no_calulate[0]),as_dict=True)
        else:
            search_investors_list = frappe.db.sql(""" SELECT si.* FROM `tabSearch Investors` si  LEFT JOIN `tabInvestor Funding Stages` fs ON si.name = fs.parent 
                            WHERE fs.funding_stages IN %s AND si.investor_title LIKE %s  ORDER BY name ASC LIMIT %s OFFSET %s """, (funding_stages_tuple,'%' + search_key + '%',page_no_calulate[1], page_no_calulate[0]), as_dict=True)
        for investors_details in search_investors_list:    
            favourite_investor = frappe.db.get_value("Search Investors Favourites",{"user_id":user_id,"investors":investors_details.name},['favourites_status'])
            if favourite_investor == 1:
                favourites_status = True
            else:
                favourites_status = False    
            if investors_details.investor_logo:
                image_url = get_domain_name() + investors_details.get('investor_logo')
            else:
                image_url = ""      
            fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':investors_details.name},['funding_stages'])
            investors_list = {
                "id":investors_details.name,
                "name":investors_details.name,
                "favourites_status":favourites_status,
                "title":investors_details.investor_title or "",
                "logo":image_url,
                "investor_verified":investors_details.investor_verified or "",
                "linkedin":investors_details.investor_linkedin or "",
                "website":investors_details.investor_website or "",
                "about_us":investors_details.about_us or "",
                "value_add":investors_details.value_add or "",
                "firm_type":investors_details.firm_type or "",
                "hq":investors_details.hq or "",
                "funding_requirements":investors_details.funding_requirements or "",
                "funding_stages_table":fund_rasing,          
                "min_check_size":investors_details.min_check_size or "0",
                "max_check_size":investors_details.max_check_size or "0"
            }
            search_bar_investors_list.append(investors_list)
        return {"status":True,"investors_count":investors_count[0]["investor_counts"],"search_bar":search_bar_investors_list}    
    except Exception as e:
        return {"status":False,"message":e}