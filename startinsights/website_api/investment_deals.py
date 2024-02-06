import frappe
from frappe.utils import now, getdate, today, format_date
from datetime import datetime
import html2text
from frappe.utils import  get_url


# investment deals list view
@frappe.whitelist()
def investment_deals_details():
    image_url = ""
    web_url = ""
    doc1 = ""
    doc2 = ""
    doc3 = ""
    plain_text_description = ""
    try:
        investment_api = frappe.get_all('Investment Deals',fields=['*']) 
        # Format the response
        formatted_investment_list = []
        for investment_deals in investment_api:
            plain_text_description = html2text.html2text(investment_deals.description).strip()
            if investment_deals.company_logo:
                image_url = get_url() + investment_deals.company_logo
            else:
                image_url = ""
            if investment_deals.doc1:
                doc1 = get_url() +  investment_deals.doc1
            else:
                doc1 = ""   
            if investment_deals.doc2:
                doc2 = get_url() + investment_deals.doc2
            else:
                doc2 = ""
            if investment_deals.doc3:
                doc3 = get_url() + investment_deals.doc3
            else:
                doc3 = ""                 
            investment_deals_data = {
                'id': investment_deals.name,
                'name': investment_deals.name,
                'Legal Name': investment_deals.legal_name,
                'Founded Year': investment_deals.founded_year,
                'Website': investment_deals.website,
                'Company Logo': image_url ,
                'description': plain_text_description,
                'linkedin': investment_deals.linkedin,
                'youtube': investment_deals.youtube or "",
                'facebook': investment_deals.facebook or "",
                'instagram': investment_deals.instagram or "",
                'document_1': doc1,
                'document_2': doc2,
                'document_3': doc3,
                'investment_details': []
            }
            # Fetch items for each investment deal
            investment_deals_details = frappe.get_all('Investment Team', filters={'parent': investment_deals.name},
                                                      fields=['investor_name', 'designation', 'linkedin'])
            for invest in investment_deals_details:
                investment_deals_data['investment_details'].append({
                    'investor_name': invest.investor_name,
                    'designation': invest.designation,
                    'linkedin': invest.linkedin,
                })
            formatted_investment_list.append(investment_deals_data)
        return {"status": True, "investment_deals": formatted_investment_list}
    except Exception as e:
        frappe.log_error(f"Error in investment_deals_list: {e}")
        return {"status": False, "message": str(e)}
