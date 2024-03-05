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
                    "title":investors_details.investor_title,
                    "logo":image_url,
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
    min_count = (int(page_count) - 1) * 10
    max_count = min_count + 10
    return min_count, max_count