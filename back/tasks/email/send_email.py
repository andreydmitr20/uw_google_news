import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import config


# go to gmail/security/2-way auth/app passwords and get 16 chars password
def send_email(subject, body, to_email):
    # Email configuration
    sender_email = config.sender_email
    sender_password = config.sender_email_pass

    # Create a message object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Attach body to the email
    message.attach(MIMEText(body, "plain"))

    # Establish a connection to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, to_email, message.as_string())


if __name__ == "__main__":
    # Example usage
    send_email(
        "Test Subject", "Hello, this is a test email.", "andreydmitr21@gmail.com"
    )
