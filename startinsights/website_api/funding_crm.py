import frappe
from startinsights.custom import get_domain_name
from frappe.utils import now, getdate, today, format_date


#listed the funding crm status wise data
@frappe.whitelist()
def get_funding_crm(user_id):
    funding_max_count = "0"
    try:
        funding_crm_list = []
        funding_max_count =  get_max_funding_count(user_id)
        crm = {
            "sortlist":get_sortlist_investor(user_id),
            "contacted":get_contacted_investor(user_id),
            "pitched":get_pitched_investor(user_id),
            "diligence":get_diligence_investor(user_id),
            "won":get_won_investor(user_id),
            "lost":get_lost_investor(user_id)
        }
        funding_crm_list.append(crm)   
        return {"status":True,"funding_max_count":funding_max_count,"funding_crm_list":funding_crm_list}     
    except Exception as e:
        return {"status":False,"message":e}

#sortlist data
def get_sortlist_investor(user_id):
    sortlist_investor = []
    sortlist_count = frappe.db.sql(""" SELECT COUNT(name) AS sortlist_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'SHORTLIST'""", (user_id,), as_dict=1) or 0
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
    search_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors Favourites","funding_crm_status":"SHORTLIST","disabled":0},['*'])
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
            "investor_name":get_search_investor.investor_title or "",
            "status":"SHORTLIST",
            "contacted_person":"",
            "funding_stage":fund_rasing or [],
            "description":get_search_investor.about_us or "",      
            "website":get_search_investor.investor_website or "", 
            "mail_address":"",
            "contact_no":"",
            "notes":""
        }
        search_investor_list.append(search_investor)
    return search_investor_list    

def get_sortlist_as_user_created_investor(user_id):
    user_created_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"SHORTLIST","disabled":0},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        if user_investor.investor_logo:
            image_url = get_domain_name() + user_investor.get('investor_logo')
        else:
            image_url = ""  
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":image_url,
            "investor_name":user_investor.investor_name or "",
            "status":"SHORTLIST",
            "contacted_person":user_investor.contact_person or "",
            "funding_stage":user_investor.funding_stage or "",
            "description":user_investor.description or "",      
            "website":user_investor.website or "", 
            "mail_address":user_investor.investor_email or "",
            "contact_no":user_investor.contact_no or "",
            "notes":user_investor.notes or ""
        }
        user_created_investor_list.append(user_created_investor)
    return user_created_investor_list 

def get_contacted_as_search_investor(user_id):
    search_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors Favourites","funding_crm_status":"CONTACTED","disabled":0},['*'])
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
            "investor_name":get_search_investor.investor_title or "",
            "status":"CONTACTED",
            "contacted_person":"",
            "funding_stage":fund_rasing or [],
            "description":get_search_investor.about_us or "",      
            "website":get_search_investor.investor_website or "", 
            "mail_address":"",
            "contact_no":"",
            "notes":""
        }
        search_investor_list.append(search_investor)
    return search_investor_list    

def get_contacted_as_user_created_investor(user_id):
    user_created_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"CONTACTED","disabled":0},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        if user_investor.investor_logo:
            image_url = get_domain_name() + user_investor.get('investor_logo')
        else:
            image_url = ""  
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":image_url,
            "investor_name":user_investor.investor_name or "",
            "status":"CONTACTED",
            "contacted_person":user_investor.contact_person or "",
            "funding_stage":user_investor.funding_stage or "",
            "description":user_investor.description or "",      
            "website":user_investor.website or "", 
            "mail_address":user_investor.investor_email or "",
            "contact_no":user_investor.contact_no or "",
            "notes":user_investor.notes or ""
        }
        user_created_investor_list.append(user_created_investor)
    return user_created_investor_list    

def get_pitched_as_search_investor(user_id):
    search_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors Favourites","funding_crm_status":"PITCHED","disabled":0},['*'])
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
            "investor_name":get_search_investor.investor_title or "",
            "status":"PITCHED",
            "contacted_person":"",
            "funding_stage":fund_rasing or [],
            "description":get_search_investor.about_us or "",      
            "website":get_search_investor.investor_website or "", 
            "mail_address":"",
            "contact_no":"",
            "notes":""
        }
        search_investor_list.append(search_investor)
    return search_investor_list    

def get_pitched_as_user_created_investor(user_id):
    user_created_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"PITCHED","disabled":0},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        if user_investor.investor_logo:
            image_url = get_domain_name() + user_investor.get('investor_logo')
        else:
            image_url = ""  
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":image_url,
            "investor_name":user_investor.investor_name or "",
            "status":"PITCHED",
            "contacted_person":user_investor.contact_person or "",
            "funding_stage":user_investor.funding_stage or "",
            "description":user_investor.description or "",      
            "website":user_investor.website or "", 
            "mail_address":user_investor.investor_email or "",
            "contact_no":user_investor.contact_no or "",
            "notes":user_investor.notes or ""
        }
        user_created_investor_list.append(user_created_investor)
    return user_created_investor_list    

def get_diligence_as_search_investor(user_id):
    search_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors Favourites","funding_crm_status":"DILIGENCE","disabled":0},['*'])
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
            "investor_name":get_search_investor.investor_title or "",
            "status":"DILIGENCE",
            "contacted_person":"",
            "funding_stage":fund_rasing or [],
            "description":get_search_investor.about_us or "",      
            "website":get_search_investor.investor_website or "", 
            "mail_address":"",
            "contact_no":"",
            "notes":""
        }
        search_investor_list.append(search_investor)
    return search_investor_list    

def get_diligence_as_user_created_investor(user_id):
    user_created_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"DILIGENCE","disabled":0},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        if user_investor.investor_logo:
            image_url = get_domain_name() + user_investor.get('investor_logo')
        else:
            image_url = ""  
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":image_url,
            "investor_name":user_investor.investor_name or "",
            "status":"DILIGENCE",
            "contacted_person":user_investor.contact_person or "",
            "funding_stage":user_investor.funding_stage or "",
            "description":user_investor.description or "",      
            "website":user_investor.website or "", 
            "mail_address":user_investor.investor_email or "",
            "contact_no":user_investor.contact_no or "",
            "notes":user_investor.notes or ""
        }
        user_created_investor_list.append(user_created_investor)
    return user_created_investor_list 

def get_won_as_search_investor(user_id):
    search_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors Favourites","funding_crm_status":"WON","disabled":0},['*'])
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
            "investor_name":get_search_investor.investor_title or "",
            "status":"WON",
            "contacted_person":"",
            "funding_stage":fund_rasing or [],
            "description":get_search_investor.about_us or "",      
            "website":get_search_investor.investor_website or "", 
            "mail_address":"",
            "contact_no":"",
            "notes":""
        }
        search_investor_list.append(search_investor)
    return search_investor_list    

def get_won_as_user_created_investor(user_id):
    user_created_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"WON","disabled":0},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        if user_investor.investor_logo:
            image_url = get_domain_name() + user_investor.get('investor_logo')
        else:
            image_url = ""  
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":image_url,
            "investor_name":user_investor.investor_name or "",
            "status":"WON",
            "contacted_person":user_investor.contact_person or "",
            "funding_stage":user_investor.funding_stage or "",
            "description":user_investor.description or "",      
            "website":user_investor.website or "", 
            "mail_address":user_investor.investor_email or "",
            "contact_no":user_investor.contact_no or "",
            "notes":user_investor.notes or ""
        }
        user_created_investor_list.append(user_created_investor)
    return user_created_investor_list    

def get_lost_as_search_investor(user_id):
    search_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors Favourites","funding_crm_status":"LOST","disabled":0},['*'])
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
            "investor_name":get_search_investor.investor_title or "",
            "status":"LOST",
            "contacted_person":"",
            "funding_stage":fund_rasing or [],
            "description":get_search_investor.about_us or "",      
            "website":get_search_investor.investor_website or "", 
            "mail_address":"",
            "contact_no":"",
            "notes":""
        }
        search_investor_list.append(search_investor)
    return search_investor_list    

def get_lost_as_user_created_investor(user_id):
    user_created_investor_list = []
    funding_crm = frappe.db.get_all("Funding CRM",{"user_id":user_id,"type_of_investor":"User Created Investors","funding_crm_status":"LOST","disabled":0},['*'])
    for crm in funding_crm:
        user_investor = frappe.get_doc("User Created Investors",crm.user_created_investor)
        if user_investor.investor_logo:
            image_url = get_domain_name() + user_investor.get('investor_logo')
        else:
            image_url = ""  
        user_created_investor = {
            "id":user_investor.name,
            "name":user_investor.name,
            "type_of_investor":"User Created Investors",
            "logo":image_url,
            "investor_name":user_investor.investor_name or "",
            "status":"LOST",
            "contacted_person":user_investor.contact_person or "",
            "funding_stage":user_investor.funding_stage or "",
            "description":user_investor.description or "",      
            "website":user_investor.website or "", 
            "mail_address":user_investor.investor_email or "",
            "contact_no":user_investor.contact_no or "",
            "notes":user_investor.notes or ""
        }
        user_created_investor_list.append(user_created_investor)
    return user_created_investor_list   

def get_max_funding_count(user_id):
    sortlist_count = frappe.db.sql(""" SELECT COUNT(name) AS sortlist_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'SHORTLIST'""", (user_id,), as_dict=1) or 0
    contacted_investor_count = frappe.db.sql(""" SELECT COUNT(name) AS contacted_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'CONTACTED'""", (user_id,), as_dict=1) or 0
    pitched_investor_count = frappe.db.sql(""" SELECT COUNT(name) AS pitched_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'PITCHED'""", (user_id,), as_dict=1) or 0
    diligence_investor_count = frappe.db.sql(""" SELECT COUNT(name) AS diligence_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'DILIGENCE'""", (user_id,), as_dict=1) or 0
    won_investor_count = frappe.db.sql(""" SELECT COUNT(name) AS won_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'WON'""", (user_id,), as_dict=1) or 0
    lost_investor_count = frappe.db.sql(""" SELECT COUNT(name) AS lost_count FROM `tabFunding CRM` WHERE user_id = %s AND funding_crm_status = 'LOST'""", (user_id,), as_dict=1) or 0
    max_count_funding_count = max(sortlist_count[0]['sortlist_count'], contacted_investor_count[0]['contacted_count'],pitched_investor_count[0]['pitched_count'],diligence_investor_count[0]['diligence_count'],won_investor_count[0]['won_count'],lost_investor_count[0]['lost_count'])
    return max_count_funding_count

#funding crm status update api
@frappe.whitelist()
def update_funding_crm(investor_id,user_id,investor_status,type_of_investor):
    status = ""
    message = ""
    try:
        if type_of_investor == "Search Investors":
            funding_crm_search_investor = frappe.db.get_value("Funding CRM",{"user_id":user_id,"type_of_investor":"Search Investors Favourites","search_investor_id":investor_id},['name'])
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

@frappe.whitelist()
def delete_funding_crm_investor(user_id,type_of_investor,investor_id,delete_status):
    try:
        if type_of_investor == "Search Investors Favourites":
            get_funding_crm_id = frappe.db.get_value("Funding CRM",{"user_id":user_id,"type_of_investor":type_of_investor,"search_investor_id":investor_id},['name'])
            funding_crm = frappe.get_doc("Funding CRM",get_funding_crm_id)
            funding_crm.disabled = delete_status
            funding_crm.save()
            frappe.db.commit()
        elif type_of_investor == "User Created Investors":
            get_funding_crm_id = frappe.db.get_value("Funding CRM",{"user_id":user_id,"type_of_investor":type_of_investor,"user_created_investor":investor_id},['name'])
            funding_crm = frappe.get_doc("Funding CRM",get_funding_crm_id) 
            funding_crm.disabled = delete_status
            funding_crm.save()
            frappe.db.commit()
        return {"status":True,"message":"Success"}
    except Exception as e:
        return {"status":False,"message":e}