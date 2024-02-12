from frappe import _
import frappe

def get_long_url(short_url):
    # Query the database to find the long URL based on the short URL
    # Replace this with your actual query logic
    doc = frappe.get_doc("Shorter Url", {"short_url": short_url})

    if doc:
        return doc.long_url
    else:
        return None

@frappe.whitelist(allow_guest=True)
def redirect_to_long_url(short_url):

    print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    # Get the long URL associated with the short URL
    long_url = get_long_url(short_url)
    if long_url:
        # Perform a 302 (temporary) redirect to the long URL
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = long_url
    else:
        # Handle case when short URL is not found (e.g., show an error page)
        frappe.throw(_("Short URL not found"), title=_("Error"))