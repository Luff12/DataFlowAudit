import smtplib
import os

from email.message import EmailMessage


# Send email notification
def send_email(subject, message):

    sender_email = os.getenv("EMAIL_ADDRESS")

    sender_password = os.getenv("EMAIL_APP_PASSWORD")

    receiver_email = os.getenv("ALERT_RECEIVER")

    # Check email settings
    if not sender_email or not sender_password or not receiver_email:

        print("Email not configured.")

        print("Alert:", message)

        return False

    try:

        email = EmailMessage()

        email["Subject"] = subject

        email["From"] = sender_email

        email["To"] = receiver_email

        email.set_content(message)

        # Connect to Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(sender_email, sender_password)

        server.send_message(email)

        server.quit()

        print("Email sent successfully!")

        return True

    except Exception as error:

        print("Email error:", error)

        return False
