import frappe
from startinsights.custom import get_domain_name


@frappe.whitelist()
def get_search_investors_list(page_no,country,funding_stage,amount):
    search_investors = []
    image_url = ""
    try:
        investors_count = frappe.db.count("Search Investors",{"disabled":0})
        page_no_calulate = calculate_count(page_no)

        search_investors_list = frappe.db.sql(""" SELECT * FROM `tabSearch Investors` ORDER BY name ASC LIMIT %s OFFSET %s """, (page_no_calulate[1], page_no_calulate[0]), as_dict=True)

        search_investors = []

        for investor in search_investors_list: 
            if country:
                get_investors = frappe.db.sql(""" SELECT * FROM `tabSearch Investors` WHERE  name = %s and hq = %s ORDER BY name ASC """, (investor.name,country), as_dict=True)

            elif funding_stage:
                get_investors = frappe.db.sql("""SELECT si.*FROM `tabSearch Investors` si LEFT JOIN `tabInvestor Funding Stages` fs ON si.name = fs.parent WHERE si.name = %s AND fs.funding_stages = %s
                            ORDER BY name ASC    """, (investor.name,funding_stage), as_dict=True)
                
            elif amount:
                get_investors =  frappe.db.sql(""" SELECT * FROM `tabSearch Investors` WHERE  name = %s and max_check_size = %s ORDER BY name ASC """, (investor.name,amount), as_dict=True)
                
            elif country and funding_stage:
                get_investors = frappe.db.sql("""SELECT si.*FROM `tabSearch Investors` si LEFT JOIN `tabInvestor Funding Stages` fs ON si.name = fs.parent WHERE si.name = %s AND si.hq = %s AND fs.funding_stages = %s
                            ORDER BY name ASC    """, (investor.name,country,funding_stage), as_dict=True) 
                
            elif funding_stage and amount:
                get_investors = frappe.db.sql("""SELECT si.*FROM `tabSearch Investors` si LEFT JOIN `tabInvestor Funding Stages` fs ON si.name = fs.parent WHERE si.name = %s AND si.max_check_size = %s AND fs.funding_stages = %s
                            ORDER BY name ASC   """, (investor.name,amount,funding_stage), as_dict=True) 
                
            elif amount and country:
                get_investors = frappe.db.sql(""" SELECT * FROM `tabSearch Investors` WHERE  name = %s AND max_check_size = %s AND hq = '%s' ORDER BY name ASC """, (investor.name,amount,country), as_dict=True)

            elif country and amount and funding_stage:
                get_investors = frappe.db.sql("""SELECT si.*FROM `tabSearch Investors` si LEFT JOIN `tabInvestor Funding Stages` fs ON si.name = fs.parent WHERE si.name = %s AND si.hq = %s AND si.max_check_size = %s AND fs.funding_stages = %s
                            ORDER BY name ASC   """, (investor.name,country,amount,funding_stage), as_dict=True)       
                            
            else:
                get_investors = frappe.db.sql(""" SELECT * FROM `tabSearch Investors` WHERE name = %s ORDER BY name ASC """, (investor.name), as_dict=True)

            for investors_details in get_investors:
                if investor.investor_logo:
                    image_url = get_domain_name() + investors_details.get('investor_logo')
                else:
                    image_url = ""    
                fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':investors_details.name},['funding_stages'])

                investors_list = {
                    "id":investors_details.name,
                    "name":investors_details.name,
                    "favourites_status":False,
                    "title":investors_details.investor_title,
                    "logo":image_url,
                    "contact_no":investors_details.contact_no,
                    "investor_verified":investors_details.investor_verified,
                    "linkedin":investor.investor_linkedin,
                    "website":investor.investor_website,
                    "about_us":investor.about_us,
                    "value_add":investor.value_add,
                    "firm_type":investor.firm_type,
                    "hq":investor.hq or "",
                    "funding_requirements":investor.funding_requirements,
                    "funding_stages_table":fund_rasing,          
                    "min_check_size":investor.min_check_size,
                    "max_check_size":investor.max_check_size
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
                "title":get_search_investors_list.investor_title,
                "logo":image_url,
                "investor_verified":get_search_investors_list.investor_verified,
                "linkedin":get_search_investors_list.investor_linkedin,
                "website":get_search_investors_list.investor_website,
                "about_us":get_search_investors_list.about_us,
                "value_add":get_search_investors_list.value_add,
                "firm_type":get_search_investors_list.firm_type,
                "hq":get_search_investors_list.hq or "",
                "funding_requirements":get_search_investors_list.funding_requirements,
                "funding_stages_table":fund_rasing,          
                "min_check_size":get_search_investors_list.min_check_size,
                "max_check_size":get_search_investors_list.max_check_size
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
    try:
        search_investors_list = frappe.db.sql(""" SELECT name FROM `tabSearch Investors` ORDER BY recommended_investors_count DESC """,as_dict=1)
        for investors_details in search_investors_list:
            if investors_details.investor_logo:
                image_url = get_domain_name() + investors_details.get('investor_logo')
            else:
                image_url = ""    
            fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':investors_details.name},['funding_stages'])

            investors_list = {
                "id":investors_details.name,
                "name":investors_details.name,
                "title":investors_details.investor_title,
                "logo":image_url,
                "contact_no":investors_details.contact_no,
                "investor_verified":investors_details.investor_verified,
                "linkedin":investors_details.investor_linkedin,
                "website":investors_details.investor_website,
                "about_us":investors_details.about_us,
                "value_add":investors_details.value_add,
                "firm_type":investors_details.firm_type,
                "hq":investors_details.hq or "",
                "funding_requirements":investors_details.funding_requirements,
                "funding_stages_table":fund_rasing,          
                "min_check_size":investors_details.min_check_size,
                "max_check_size":investors_details.max_check_size
            }
            search_investors.append(investors_list) 
        return {"status":True,"message":search_investors_list}
    except Exception as e:
        return {"status":False,"message":e}