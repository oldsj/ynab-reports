from PIL import Image, ImageFont, ImageDraw 
from ynab.reporting import *
from mail import *

payee = "starbucks"
total_sbx = f"${calculate_payee_yearly(payee, 2022) * -1}"
image = Image.open("./assets/sbx.jpeg")
text = f"""You thirsty betch
you spent {total_sbx} 
on {payee} this year"""
font = ImageFont.truetype("./assets/JetBrainsMono-ExtraBold.ttf", 80)
image_editable = ImageDraw.Draw(image)

image_editable.text((15,15), text, fill=(255, 102, 102), font=font, )

# resize
basewidth = 400
wpercent = (basewidth/float(image.size[0]))
hsize = int((float(image.size[1])*float(wpercent)))
sbux = image.resize((basewidth,hsize), Image.Resampling.LANCZOS)

email.send(
    sender=f"{mail_sender} <{mail_user}>",
    receivers=recipients,
    subject="YNAB Wrapped",
    html_template="templates/wrapped.html.j2",
    body_images={
        "sbux": sbux,
    }
)
