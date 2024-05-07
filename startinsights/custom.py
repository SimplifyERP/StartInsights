import frappe
from urllib.parse import quote,urlparse
from frappe.utils.pdf import get_pdf


def get_domain_name():
    site = frappe.get_site_path()
    if site == "./admin.startinsights.io" :
        url = "https://admin.startinsights.io."
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc
        return f"https://{domain_name}"
    elif site == "./stage.startinsights.ai":
        url = "https://stage.startinsights.io."
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc
        return f"https://{domain_name}"
    elif site == "./core.startinsights.io":
        url = "https://core.startinsights.io."
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc
        return f"https://{domain_name}"

