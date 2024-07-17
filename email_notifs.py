import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from letter_work_around import registrant_letter, admin_letter
import os


def send_email(firstname, lastname, recipient_email, phone, registration_type, snack_preferences, extra_services):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_email_app_pass = os.getenv('SENDER_EMAIL_APP_PASS')  # Use your app password here
    admin_email = os.getenv('ADMIN_EMAIL')
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # For SSL: 465, For TLS: 587

    registrant_message = MIMEMultipart()
    registrant_message['From'] = sender_email
    registrant_message['To'] = recipient_email
    registrant_message['Subject'] = f"Confirmation Of Registration For Speech Conference {datetime.now().year}"

    admin_message = MIMEMultipart()
    admin_message['From'] = sender_email
    admin_message['To'] = admin_email
    admin_message['Subject'] = "Registration Alert!!!"

    registrant_notif_body = registrant_letter(firstname, lastname, registration_type, snack_preferences, extra_services)
    admin_notif_body = admin_letter(firstname, lastname, recipient_email, phone, registration_type, snack_preferences,
                                    extra_services)

    # Attach the email body content
    registrant_message.attach(MIMEText(registrant_notif_body, 'plain'))
    admin_message.attach(MIMEText(admin_notif_body, 'plain'))

    try:
        # Create a SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(sender_email, sender_email_app_pass)  # Login to SMTP server

        # Send email
        server.sendmail(sender_email, recipient_email, registrant_message.as_string())
        server.sendmail(sender_email, admin_email, admin_message.as_string())
        server.close()
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {str(e)}')
