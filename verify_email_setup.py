import smtplib
import sys
import os

# Add current directory to path so we can import email_config
sys.path.append(os.getcwd())

try:
    import email_config
except ImportError:
    print("❌ Could not import email_config.py. Make sure it exists in the current directory.")
    sys.exit(1)

def verify():
    print("="*50)
    print("EMAIL CONFIGURATION VERIFICATION")
    print("="*50)
    print(f"Email: {email_config.SENDER_EMAIL}")
    # Mask password for display
    masked_pw = "*" * len(email_config.SENDER_PASSWORD) if email_config.SENDER_PASSWORD else "[EMPTY]"
    print(f"Password: {masked_pw}")
    print(f"Server: {email_config.SMTP_SERVER}:{email_config.SMTP_PORT}")
    print("-" * 50)

    if not email_config.SENDER_PASSWORD:
        print("❌ Error: Password is empty.")
        return False

    try:
        print(f"Connecting to {email_config.SMTP_SERVER}...")
        server = smtplib.SMTP(email_config.SMTP_SERVER, email_config.SMTP_PORT)
        server.starttls()
        
        print("Attempting login...")
        server.login(email_config.SENDER_EMAIL, email_config.SENDER_PASSWORD)
        
        print("\n✅ Login SUCCESSFUL!")
        print("The password is correct and accepted by the server.")
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("\n❌ Login FAILED: Authentication Error")
        print(f"Server response: {e}")
        print("\nPossible causes:")
        print("1. Incorrect email or password")
        print("2. You are using your normal Gmail password instead of an APP PASSWORD")
        print("   -> You MUST generate an App Password if using Gmail with 2FA.")
        print("3. 2-Step Verification is not enabled")
    except Exception as e:
        print(f"\n❌ Connection FAILED: {str(e)}")
    
    return False

if __name__ == "__main__":
    verify()
