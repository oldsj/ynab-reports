import os
from redmail import EmailSender
from dotenv import load_dotenv
from ynab.reporting import *

load_dotenv()

# TODO handle missing or improper env
recipients = os.getenv("MAIL_RECIPIENTS")
recipients = recipients.split(",")

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


def send_report(fig, time_to_fi: str):
    year = 2022
    month = 11
    float_format = "%.2f"
    df_financial_snapshot = calculate_financial_snapshot(year=year, month=month)
    snapshot = df_financial_snapshot.to_html()
    df_top_in, df_top_out = get_top_flows(year=year, month=month, n_rows=10)
    top_inflows = df_top_in.to_html()
    top_outflows = df_top_out.to_html()

    email.send(
        sender=f"{mail_sender} <{mail_user}>",
        subject="YNAB Report",
        html_template="templates/report.html.j2",
        body_images={
            "fi_plot": fig,
        },
        body_params={
            "time_to_fi": time_to_fi,
            "top_inflows": top_inflows,
            "top_outflows": top_outflows,
            "snapshot": snapshot
        }
    )
