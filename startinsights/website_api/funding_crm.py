import frappe
from startinsights.custom import get_domain_name
from frappe.utils import now, getdate, today, format_date


#listed the funding crm status wise data
@frappe.whitelist()
def get_funding_crm(user_id):
    try:
        funding_crm_list = []
        crm = {
            "sortlist":get_sortlist_investor(user_id),
            "contacted":get_contacted_investor(user_id),
            "pitched":get_pitched_investor(user_id),
            "diligence":get_diligence_investor(user_id),
            "won":get_won_investor(user_id),
            "lost":get_lost_investor(user_id)
        }
        funding_crm_list.append(crm)   
        return {"status":True,"funding_crm_list":funding_crm_list}     
    except Exception as e:
        return {"status":False,"message":e}

#sortlist data
def get_sortlist_investor(user_id):
    sortlist_investor = []
    sortlist_count = frappe.db.sql(""" SELECT COUNT(name) AS sortlist_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'SORTLIST'""", (user_id,), as_dict=1) or 0
    sortlist_investor = {
        "search_investor":get_sortlist_as_search_investor(user_id),
        "user_created_investor":get_sortlist_as_user_created_investor(user_id),
        "sortlist_count":sortlist_count[0]['sortlist_count']
    }
    return sortlist_investor

#contacted data
def get_contacted_investor(user_id):
    contacted_investor = []
    contacted_investor_count = frappe.db.sql(""" SELECT COUNT(name) AS contacted_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'CONTACTED'""", (user_id,), as_dict=1) or 0
    contacted_investor = {
        "search_investor":get_contacted_as_search_investor(user_id),
        "user_created_investor":get_contacted_as_user_created_investor(user_id),
        "contacted_count":contacted_investor_count[0]['contacted_count']
    }
    return contacted_investor

#pitched data
def get_pitched_investor(user_id):
    pitched_investor = []
    pitched_investor_count = frappe.db.sql(""" SELECT COUNT(name) AS pitched_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'PITCHED'""", (user_id,), as_dict=1) or 0
    pitched_investor = {
        "search_investor":get_pitched_as_search_investor(user_id),
        "user_created_investor":get_pitched_as_user_created_investor(user_id),
        "pitched_count":pitched_investor_count[0]['pitched_count']
    }
    return pitched_investor

#diligence data
def get_diligence_investor(user_id):
    diligence_investor = []
    diligence_investor_count = frappe.db.sql(""" SELECT COUNT(name) AS diligence_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'DILIGENCE'""", (user_id,), as_dict=1) or 0
    diligence_investor = {
        "search_investor":get_diligence_as_search_investor(user_id),
        "user_created_investor":get_diligence_as_user_created_investor(user_id),
        "diligence_count":diligence_investor_count[0]['diligence_count']
    }
    return diligence_investor

#won data
def get_won_investor(user_id):
    won_investor = []
    won_investor_count = frappe.db.sql(""" SELECT COUNT(name) AS won_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'WON'""", (user_id,), as_dict=1) or 0
    won_investor = {
        "search_investor":get_won_as_search_investor(user_id),
        "user_created_investor":get_won_as_user_created_investor(user_id),
        "won_count":won_investor_count[0]['won_count']
    }
    return won_investor

#lost data
def get_lost_investor(user_id):
    lost_investor = []
    lost_investor_count = frappe.db.sql(""" SELECT COUNT(name) AS lost_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'LOST'""", (user_id,), as_dict=1) or 0
    lost_investor = {
        "search_investor":get_lost_as_search_investor(user_id),
        "user_created_investor":get_lost_as_user_created_investor(user_id),
        "lost_count":lost_investor_count[0]['lost_count']
    }
    return lost_investor

def get_sortlist_as_search_investor(user_id):
    search_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors","funding_crm_status":"SORTLIST"},['*'])
    for crm in funding_crm:
        get_search_investor = frappe.get_doc("Search Investors",crm.search_investor_id)
        fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':get_search_investor.name},['funding_stages'])
        if get_search_investor.investor_logo:
            image_url = get_domain_name() + get_search_investor.get('investor_logo')
        else:
            image_url = ""  
        search_investor = {
            "id":get_search_investor.name,
            "name":get_search_investor.name,
            "type_of_investor":"Search Investors",
            "logo":image_url,
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":fund_rasing,
            "description":get_search_investor.about_us,      
            "website":get_search_investor.investor_website, 
            "mail_address":"",
            "contact_no":"",
        }
    return search_investor    

def get_sortlist_as_user_created_investor(user_id):
    user_created_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"SORTLIST"},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":"",
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":"",
            "description":user_investor.notes,      
            "website":"", 
            "mail_address":user_investor.investor_email,
            "contact_no":"",
        }
    return user_created_investor 

def get_contacted_as_search_investor(user_id):
    search_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors","funding_crm_status":"CONTACTED"},['*'])
    for crm in funding_crm:
        get_search_investor = frappe.get_doc("Search Investors",crm.search_investor_id)
        fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':get_search_investor.name},['funding_stages'])
        if get_search_investor.investor_logo:
            image_url = get_domain_name() + get_search_investor.get('investor_logo')
        else:
            image_url = ""  
        search_investor = {
            "id":get_search_investor.name,
            "name":get_search_investor.name,
            "type_of_investor":"Search Investors",
            "logo":image_url,
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":fund_rasing,
            "description":get_search_investor.about_us,      
            "website":get_search_investor.investor_website, 
            "mail_address":"",
            "contact_no":"",
        }
    return search_investor    

def get_contacted_as_user_created_investor(user_id):
    user_created_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"CONTACTED"},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":"",
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":"",
            "description":user_investor.notes,      
            "website":"", 
            "mail_address":user_investor.investor_email,
            "contact_no":"",
        }
    return user_created_investor    

def get_pitched_as_search_investor(user_id):
    search_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors","funding_crm_status":"PITCHED"},['*'])
    for crm in funding_crm:
        get_search_investor = frappe.get_doc("Search Investors",crm.search_investor_id)
        fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':get_search_investor.name},['funding_stages'])
        if get_search_investor.investor_logo:
            image_url = get_domain_name() + get_search_investor.get('investor_logo')
        else:
            image_url = ""  
        search_investor = {
            "id":get_search_investor.name,
            "name":get_search_investor.name,
            "type_of_investor":"Search Investors",
            "logo":image_url,
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":fund_rasing,
            "description":get_search_investor.about_us,      
            "website":get_search_investor.investor_website, 
            "mail_address":"",
            "contact_no":"",
        }
    return search_investor    

def get_pitched_as_user_created_investor(user_id):
    user_created_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"PITCHED"},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":"",
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":"",
            "description":user_investor.notes,      
            "website":"", 
            "mail_address":user_investor.investor_email,
            "contact_no":"",
        }
    return user_created_investor    

def get_pitched_as_search_investor(user_id):
    search_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors","funding_crm_status":"PITCHED"},['*'])
    for crm in funding_crm:
        get_search_investor = frappe.get_doc("Search Investors",crm.search_investor_id)
        fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':get_search_investor.name},['funding_stages'])
        if get_search_investor.investor_logo:
            image_url = get_domain_name() + get_search_investor.get('investor_logo')
        else:
            image_url = ""  
        search_investor = {
            "id":get_search_investor.name,
            "name":get_search_investor.name,
            "type_of_investor":"Search Investors",
            "logo":image_url,
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":fund_rasing,
            "description":get_search_investor.about_us,      
            "website":get_search_investor.investor_website, 
            "mail_address":"",
            "contact_no":"",
        }
    return search_investor    

def get_pitched_as_user_created_investor(user_id):
    user_created_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"PITCHED"},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":"",
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":"",
            "description":user_investor.notes,      
            "website":"", 
            "mail_address":user_investor.investor_email,
            "contact_no":"",
        }
    return user_created_investor    

def get_diligence_as_search_investor(user_id):
    search_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors","funding_crm_status":"DILIGENCE"},['*'])
    for crm in funding_crm:
        get_search_investor = frappe.get_doc("Search Investors",crm.search_investor_id)
        fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':get_search_investor.name},['funding_stages'])
        if get_search_investor.investor_logo:
            image_url = get_domain_name() + get_search_investor.get('investor_logo')
        else:
            image_url = ""  
        search_investor = {
            "id":get_search_investor.name,
            "name":get_search_investor.name,
            "type_of_investor":"Search Investors",
            "logo":image_url,
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":fund_rasing,
            "description":get_search_investor.about_us,      
            "website":get_search_investor.investor_website, 
            "mail_address":"",
            "contact_no":"",
        }
    return search_investor    

def get_diligence_as_user_created_investor(user_id):
    user_created_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"DILIGENCE"},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":"",
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":"",
            "description":user_investor.notes,      
            "website":"", 
            "mail_address":user_investor.investor_email,
            "contact_no":"",
        }
    return user_created_investor 

def get_won_as_search_investor(user_id):
    search_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors","funding_crm_status":"WON"},['*'])
    for crm in funding_crm:
        get_search_investor = frappe.get_doc("Search Investors",crm.search_investor_id)
        fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':get_search_investor.name},['funding_stages'])
        if get_search_investor.investor_logo:
            image_url = get_domain_name() + get_search_investor.get('investor_logo')
        else:
            image_url = ""  
        search_investor = {
            "id":get_search_investor.name,
            "name":get_search_investor.name,
            "type_of_investor":"Search Investors",
            "logo":image_url,
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":fund_rasing,
            "description":get_search_investor.about_us,      
            "website":get_search_investor.investor_website, 
            "mail_address":"",
            "contact_no":"",
        }
    return search_investor    

def get_won_as_user_created_investor(user_id):
    user_created_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"WON"},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":"",
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":"",
            "description":user_investor.notes,      
            "website":"", 
            "mail_address":user_investor.investor_email,
            "contact_no":"",
        }
    return user_created_investor    

def get_lost_as_search_investor(user_id):
    search_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors","funding_crm_status":"LOST"},['*'])
    for crm in funding_crm:
        get_search_investor = frappe.get_doc("Search Investors",crm.search_investor_id)
        fund_rasing = frappe.db.get_all("Investor Funding Stages",{'parent':get_search_investor.name},['funding_stages'])
        if get_search_investor.investor_logo:
            image_url = get_domain_name() + get_search_investor.get('investor_logo')
        else:
            image_url = ""  
        search_investor = {
            "id":get_search_investor.name,
            "name":get_search_investor.name,
            "type_of_investor":"Search Investors",
            "logo":image_url,
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":fund_rasing,
            "description":get_search_investor.about_us,      
            "website":get_search_investor.investor_website, 
            "mail_address":"",
            "contact_no":"",
        }
    return search_investor    

def get_lost_as_user_created_investor(user_id):
    user_created_investor = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"LOST"},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":"",
            "status":"SORTLIST",
            "contacted_person":"",
            "funding_stage":"",
            "description":user_investor.notes,      
            "website":"", 
            "mail_address":user_investor.investor_email,
            "contact_no":"",
        }
    return user_created_investor   

#funding crm status update api
@frappe.whitelist()
def update_funding_crm(investor_id,user_id,investor_status,type_of_investor):
    status = ""
    message = ""
    try:
        if type_of_investor == "Search Investors":
            funding_crm_search_investor = frappe.db.get_value("Funding CRM",{"user_id":user_id,"type_of_investor":type_of_investor,"search_investor_id":investor_id},['name'])
            frappe.db.set_value("Funding CRM",funding_crm_search_investor,"funding_crm_status",investor_status)
            get_investor_status = frappe.get_doc("Funding CRM",funding_crm_search_investor)
            status = True
        elif type_of_investor == "User Created Investors":   
            funding_crm_user_investor = frappe.db.get_value("Funding CRM",{"user_id":user_id,"type_of_investor":type_of_investor,"user_created_investor":investor_id},['name'])
            frappe.db.set_value("Funding CRM",funding_crm_user_investor,"funding_crm_status",investor_status)
            get_investor_status = frappe.get_doc("Funding CRM",funding_crm_user_investor)
            status = True
        else:
            status = False
            message = "You Given Type of Investor No Data In Backend"    
        return {"status":status,"message":message,"funding_crm_status":get_investor_status.funding_crm_status}
    except Exception as e:
        return {"status":False,"message":e}