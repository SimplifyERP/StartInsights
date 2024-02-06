import frappe
from frappe.utils import now, getdate, today, format_date
from datetime import datetime
import html2text
from frappe.utils import  get_url
from frappe import _



# investment deals list view
@frappe.whitelist()
def investment_deals_details(id):
    image_url = ""
    web_url = ""
    doc1 = ""
    doc2 = ""
    doc3 = ""
    plain_text_description = ""
    try:
        investment_api = frappe.db.get_all("Investment Deals",{'name':id},['*'])
        # Format the response
        formatted_investment_list = []
        for investment_deals in investment_api:
            plain_text_description = html2text.html2text(investment_deals.description).strip()
            if investment_deals.company_logo:
                image_url = get_url() + investment_deals.company_logo
            else:
                image_url = ""               
            investment_deals_data = {
                'id': investment_deals.name,
                'name': investment_deals.name,
                'Legal Name': investment_deals.legal_name,
                'Company Logo': image_url ,
                'description': plain_text_description,
                'founders_list': [],
                'documents':[]
            }
            # Fetch items for each investment deal
            investment_deals_details = frappe.get_all('Investment Team', filters={'parent': investment_deals.name},
                                                      fields=['investor_name', 'designation', 'founder_logo'])
            for invest in investment_deals_details:
                if invest.founder_logo:
                    logo = get_url() + invest.founder_logo
                else:
                    logo = "" 
                investment_deals_data['founders_list'].append({
                    'investor_name': invest.investor_name,
                    'designation': invest.designation,
                    'founder_logo': logo,
                })
            investment_deals_doc = frappe.get_all('Pitch Craft Documents Table', filters={'parent': investment_deals.name},
                                                      fields=['documents_required'])
            for invested in investment_deals_doc:
                investment_deals_data['documents'].append({
                    'doc_name': invested.documents_required,
                })
            formatted_investment_list.append(investment_deals_data)
        return {"status": True, "investment_deals": formatted_investment_list}
    except Exception as e:
        frappe.log_error(f"Error in investment_deals_list: {e}")
        return {"status": False, "message": str(e)}


# investment deals list view
@frappe.whitelist(allow_guest=True)
def investment_deals_list():
    try:
        investment_api = frappe.get_all("Investment Deals", fields=['name', 'legal_name', 'company_logo'])
        # Format the response
        formatted_investment_list = []
        for investment_deal in investment_api:
            image_url = ""
            if investment_deal.company_logo:
                image_url = frappe.utils.get_url() + investment_deal.company_logo
            investment_deal_data = {
                'id': investment_deal.name,
                'name': investment_deal.name,
                'Legal Name': investment_deal.legal_name,
                'Company Logo': image_url,
            }
            formatted_investment_list.append(investment_deal_data)
        return {"status": True, "investment_deals_list": formatted_investment_list}
    except Exception as e:
        frappe.log_error(_("Error in investment_deals_list: {0}").format(e))
        return {"status": False, "message": str(e)}
