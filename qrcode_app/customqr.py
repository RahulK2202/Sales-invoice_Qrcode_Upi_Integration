import frappe
from frappe.utils import random_string, get_url
import frappe

from pibicut.pibicut.custom import get_qrcode



@frappe.whitelist()
def generate_qr_code(doc, event):
    # use doc instead of sale_invoice

    print(doc,"doc is hereeee")
    print("coming...................................>")
    # UPI ID for the payment
    upi_id = "yourupi@ybl"

    upi_url=f"upi://pay?pa={upi_id}&pn=bcbcb&am={doc.grand_total}&tn=InvoicePayment&cu=INR"
    shortener = frappe.new_doc('Shortener')
    
    short=validating_shortner()

    try:
        docs = frappe.get_value("Shortener", {"short_url": short}, "name")
        if docs:
            while True:
                docs = frappe.get_value("Shortener", {"short_url": short}, "name")
                if docs:
                    short=validating_shortner()
                else:
                    break

    except:
        pass                    


    url_short = "".join([short])
    
    print(url_short, "url shorttttttt")

    qr_code_short = get_url(url_short)
    print(qr_code_short,"shortner did")
    qr_code = get_qrcode(qr_code_short)
    print("before qr code")
    print(qr_code)
    print("after qr codeeee")
    published = True
    route = url_short

    # new_doc.
    print("upi_url....................")
    shortener.long_url=upi_url
    print("hh,,,,,,,,,,,,,,,,,,,,,,")
    print(qr_code_short,"................................")
    print("qr_code_short....................<>")
    
    shortener.short_url=get_url(url_short)
    print("yessssssssssssssssssssssssssssssss")
    shortener.qr_code=qr_code
    print(qr_code,"qrcodeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    shortener.insert()
    print("reacheddddddddddddddddddddddddddddddddd")
    doc.custom_shortner_qr_code=shortener

    doc.save()
    print("success ........................................>")
    # return the QR code image URL instead of the shortener object
    return shortener.qr_code



def validating_shortner():
    random_code = random_string(5)
    print( random_code,"random_code")
    return random_code



@frappe.whitelist()
def get_imagepath(doc, event):
    # use doc instead of shorter
    print("this is reachedddd ......................")
    # get the shortener document from the database
    if  doc.custom_shortner_qr_code:
        shortener = frappe.get_doc('Shortener', doc.custom_shortner_qr_code)
   
    # get the QR code image URL from the shortener object
        qr_code = shortener.qr_code
        print(qr_code,"this si qr_code")


        # set the custom field value to the QR code image URL
        doc.custom_qr_code = '<img src="{0}" width="140px"/>'.format(qr_code)
        # save the changes
        doc.save()

    