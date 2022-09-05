import os
from redmail import EmailSender
from dotenv import load_dotenv

load_dotenv()

recipients = os.getenv("MAIL_RECIPIENTS").split(",")
mail_user = os.getenv("MAIL_USERNAME")
mail_password = os.getenv("MAIL_PASSWORD")
mail_host = os.getenv("MAIL_SERVER")
mail_port = os.getenv("MAIL_PORT")
mail_sender = os.getenv("MAIL_DEFAULT_SENDER")

email = EmailSender(
    host=mail_host, port=mail_port, username=mail_user, password=mail_password
)
email.receivers = recipients
email.set_template_paths(html="src")


def send_report(fig):
    email.send(
        sender=f"{mail_sender} <{mail_user}>",
        subject="YNAB Report",
        html_template="report.html.j2",
        body_images={
            "report_plot": fig,
        },
    )
