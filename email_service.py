import smtplib
""" Formats the email content (plain text or HTML)."""
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
"""Allows combining multiple email components, such as 
plain text, HTML, or attachments."""




GMAIL_USER = "siddharthpal90990@gmail.com"
GMAIL_PASS = "sped iipy yvgq imlw"
NOTIFY_EMAIL = "sonupal8980@gmail.com"

def send_email(subject, body):
    """Send email notifications."""
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = NOTIFY_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        """Upgrades the connection to use 
        secure encryption (TLS). This is necessary for 
        Gmail's SMTP server."""
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())
