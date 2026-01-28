import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
try:
    import email_config
except ImportError:
    email_config = None
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_emergency_email(subject, body, recipients=None):
    """
    Sends an emergency email to the specified recipients.
    If credentials are not configured, it simulates the email sending.
    """
    if recipients is None:
        if email_config:
            recipients = email_config.STUDENT_EMAILS + email_config.STAFF_EMAILS
        else:
            recipients = []
        
        # Filter out examples if they are still there and we have real ones
        recipients = [r for r in recipients if "student" not in r and "campus.edu" not in r]
        # Always include the specific user request
        if "247r1a66a1@cmrtc.ac.in" not in recipients:
             recipients.append("247r1a66a1@cmrtc.ac.in")

    import os
    sender_email = os.environ.get("SENDER_EMAIL", email_config.SENDER_EMAIL if email_config else "your_email@gmail.com")
    sender_password = os.environ.get("SENDER_PASSWORD", email_config.SENDER_PASSWORD if email_config else "")
    smtp_server = os.environ.get("SMTP_SERVER", email_config.SMTP_SERVER if email_config else "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", email_config.SMTP_PORT if email_config else 587))

    # Check for placeholder or empty credentials
    if not sender_password or "your_" in sender_email or "your_" in sender_password:
        logger.warning("⚠️ Email credentials not configured. Simulating email send.")
        print(f"SIMULATION: Sending email to {recipients}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        return True, "Email simulation successful (Configure credentials in email_config.py)"

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = f"🚨 {subject} 🚨"

        msg.attach(MIMEText(body, 'plain'))

        # Connect to server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, recipients, text)
        server.quit()
        
        logger.info(f"✅ Email sent successfully to {len(recipients)} recipients.")
        return True, f"Email sent to {len(recipients)} recipients"
        
    except Exception as e:
        logger.error(f"❌ Failed to send email: {str(e)}")
        return False, f"Email failed: {str(e)}"
