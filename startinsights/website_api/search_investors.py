import frappe
from startinsights.custom import get_domain_name


@frappe.whitelist()
def get_search_investors_list():
    search_investors = []
    image_url = ""
    try:
        get_investors = frappe.db.get_all("Search Investors",{"disabled":0},['*'],order_by='idx ASC')
        investors_list = []
        for investor in get_investors:
            if investor.investor_logo:
                image_url = get_domain_name() + investor.investor_logo
            else:
                image_url = ""    
            fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':investor.name},['funding_stages'])
            search_investors = {
                "title":investor.investor_title,
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
            investors_list.append(search_investors)
        return {"status":True,"search_investors_list":investors_list}
    except Exception as e:
        return {"status":False,"message":e}