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



@frappe.whitelist()
def generate_qr_code(doc, event):
    # upi_id = frappe.get_value("Upi Settings",upi_id)

    try:
        # try:
            settings=frappe.get_doc("Upi Settings", "Upi Settings")
            upi_id=settings.get_password("upi_id")

            upi_url=f"upi://pay?pa={upi_id}&pn=FRESH%20HOOKS%20ENTERPRISE&am={doc.grand_total}&tn=InvoicePayment&cu=INR"
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
            # qr_code_short = get_url(url_short)
            qr_code_short = get_custom_url_without_port(url_short)
            print(qr_code_short,"qr_code_shortqr_code_short................")
            qr_code = qrcode_get(qr_code_short)

            shortener.long_url=upi_url
            shortener.short_url=get_custom_url_without_port(url_short)
            shortener.qr_code=qr_code
            shortener.published = True
            shortener.route = url_short

            shortener.insert()
            if hasattr(doc, "custom_shortner_qr_code"):
                frappe.db.set_value(doc.doctype, doc.name, "custom_shortner_qr_code", shortener.name)
            # doc.custom_shortner_qr_code=shortener
            # doc.save()
            return shortener
    except Exception as e:
        frappe.throw(f"Error: {str(e)}")





def get_custom_url_without_port(short_url):
    # Manually construct the URL without port
    site_url = frappe.utils.get_url()
    print(site_url,"site_url.............")
    parsed_url = frappe.utils.urlparse(site_url)
    print(parsed_url,"parsed_url.................")
    url_without_port = f"{parsed_url.scheme}://{parsed_url.hostname}/{short_url}"
    print(url_without_port,"url_without_port........")
    return url_without_port







        
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
    print("hello loading")
    if  doc.custom_shortner_qr_code:
        shortener = frappe.get_doc('Shorter Url', doc.custom_shortner_qr_code)
        qr_code = shortener.qr_code
        doc.custom_qr_code = '<img src="{0}" width="140px"/>'.format(qr_code)
        doc.save()




@frappe.whitelist()
def get_long_url(short_url):
    # get the long URL from the Shorter Url doctype
    long_url = frappe.db.get_value("Shorter Url", {"short_url": short_url}, "long_url")
    # return the long URL as a response
    return long_url












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
        


