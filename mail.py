import os
import yagmail
from dotenv import load_dotenv

load_dotenv()

recipients = os.getenv("MAIL_RECIPIENTS").split(",")
mail_user = os.getenv("MAIL_USERNAME")
mail_password = os.getenv("MAIL_PASSWORD")

yag = yagmail.SMTP(mail_user, mail_password)
yag.send(to=recipients, subject="YNAB Report", contents=[yagmail.inline("report.png")])
