import frappe
from frappe.utils import random_string, get_url
import frappe

# from pibicut.pibicut.custom import get_qrcode

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SquareGradiantColorMask, HorizontalGradiantColorMask, VerticalGradiantColorMask, ImageColorMask

from PIL import Image
import base64, os
from io import BytesIO

# @frappe.whitelist()
# def generate_qr_code(doc, event):
#     # use doc instead of sale_invoice

#     print(doc,"doc is hereeee")
#     print("coming...................................>")
#     # UPI ID for the payment
#     upi_id = "yourupi@ybl"

#     upi_url=f"upi://pay?pa={upi_id}&pn=bcbcb&am={doc.grand_total}&tn=InvoicePayment&cu=INR"
#     shortener = frappe.new_doc('Shortener')
    
#     short=validating_shortner()

#     try:
#         docs = frappe.get_value("Shortener", {"short_url": short}, "name")
#         if docs:
#             while True:
#                 docs = frappe.get_value("Shortener", {"short_url": short}, "name")
#                 if docs:
#                     short=validating_shortner()
#                 else:
#                     break

#     except:
#         pass                    


#     url_short = "".join([short])
    
#     print(url_short, "url shorttttttt")

#     qr_code_short = get_url(url_short)
#     print(qr_code_short,"shortner did")
#     qr_code = get_qrcode(qr_code_short)
#     print("before qr code")
#     print(qr_code)
#     print("after qr codeeee")
#     published = True
#     route = url_short

#     # new_doc.
#     print("upi_url....................")
#     print(upi_url,"this is upi")
#     shortener.long_url=upi_url
 
    

#     print(get_url(url_short),"short_url")
#     shortener.short_url=get_url(url_short)
#     print("yessssssssssssssssssssssssssssssss")
#     shortener.qr_code=qr_code

#     shortener.insert()

#     doc.custom_shortner_qr_code=shortener

#     doc.save()
#     print("success ........................................>")
#     # return the QR code image URL instead of the shortener object
#     return shortener.qr_code



@frappe.whitelist()
def generate_qr_code(doc, event):
    upi_id = "rahuljcet95@okaxis"
    upi_url=f"upi://pay?pa={upi_id}&am={doc.grand_total}&tn=InvoicePayment&cu=INR"
    shortener = frappe.new_doc('Shorter Url')  
    short=validating_shortner()

    try:
        docs = frappe.get_value("Shorter Url", {"short_url": short}, "name")
        if docs:
            while True:
                docs = frappe.get_value("Shorter Url", {"short_url": short}, "name")
                if docs:
                    short=validating_shortner()
                else:
                    break

    except:
        pass                    
    url_short = "".join([short])
    qr_code_short = get_url(url_short)
    qr_code = qrcode_get(qr_code_short)
    # published = True
    # route = url_short

    # new_doc.
    shortener.long_url=upi_url
    shortener.short_url=get_url(url_short)
    shortener.qr_code=qr_code
    shortener.insert()
    doc.custom_shortner_qr_code=shortener
    doc.save()
    return shortener
def validating_shortner():
    random_code = random_string(5)
    return random_code

def qrcode_get(input_data):
  qr = qrcode.QRCode(
        version=7,
        box_size=6,
        border=3
  )
  qr.add_data(input_data)
  qr.make(fit=True)
  img = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask(back_color = (255,255,255), center_color = (70,130,180), edge_color = (0, 0, 0)), module_drawer=GappedSquareModuleDrawer(), eye_drawer=SquareModuleDrawer())
  temp = BytesIO()
  img.save(temp, "PNG")
  temp.seek(0)
  b64 = base64.b64encode(temp.read())
  return "data:image/png;base64,{0}".format(b64.decode("utf-8"))

@frappe.whitelist()
def get_imagepath(doc, event):
    if  doc.custom_shortner_qr_code:
        shortener = frappe.get_doc('Shorter Url', doc.custom_shortner_qr_code)
        qr_code = shortener.qr_code
        doc.custom_qr_code = '<img src="{0}" width="140px"/>'.format(qr_code)
        doc.save()




@frappe.whitelist()
def redirect_to_longurl():
    # get the short URL from the request path
    short_url = frappe.request.path[1:]
    # get the Shorter Url document from the database
    shortener = frappe.get_doc('Shorter Url', {'short_url': short_url})
    # get the long URL from the Shorter Url document
    long_url = shortener.long_url
    # redirect to the long URL with a 301 response
    frappe.redirect_to(long_url, permanent=True)











# @frappe.whitelist()
# def redirect_to_longurl(short_url):
#     shortener = frappe.get_doc('Shorter Url', {'short_url': short_url})
#     print(shortener,"from redirectttttt")
#     long_url = shortener.long_url
#     # redirect to the long URL with a 301 response
#     frappe.redirect_to(long_url, permanent=True)


# # @frappe.route('/<short_url>')
# def handle_short_url(self,short_url):
#     # call the redirect function with the short URL
#     print("route is workingggg")
#     redirect_to_longurl(short_url)
        


