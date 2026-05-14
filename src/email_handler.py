import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email(to_address, subject, body):
    """Send an email via Gmail SMTP."""
    try:
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_ADDRESS
        msg["To"]      = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"Email sent to {to_address}")
        return f"Email sent to {to_address} successfully."

    except smtplib.SMTPAuthenticationError:
        return "Email authentication failed. Check your app password in settings."
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}")
        return "Failed to send email."
    except Exception as e:
        print(f"Email error: {e}")
        return "Something went wrong sending the email."

def parse_email_command(command):
    """
    Extract email parts from voice command.
    Expected: 'send email to someone@example.com about subject saying body'
    Returns: (to, subject, body) or None
    """
    try:
        # extract recipient
        if "to" not in command:
            return None
        after_to = command.split("to", 1)[1].strip()

        # extract subject
        if "about" in after_to:
            parts = after_to.split("about", 1)
            to_address = parts[0].strip()
            rest = parts[1].strip()
        else:
            return None

        # extract body
        if "saying" in rest:
            parts = rest.split("saying", 1)
            subject = parts[0].strip()
            body = parts[1].strip()
        else:
            subject = rest.strip()
            body = subject   # use subject as body if no body specified

        return to_address, subject, body

    except Exception as e:
        print(f"Email parse error: {e}")
        return None