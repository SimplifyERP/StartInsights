import frappe
from urllib.parse import quote,urlparse


def get_domain_name():
    url = "https://startinsights.ai."
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    return f"https://{domain_name}"