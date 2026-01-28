# 🚨 Emergency Alert System - Setup Guide

## What's Implemented

✅ **Emergency Alert Button** - Now fully functional!
✅ **Email Notification System** - Sends emails to all students and staff
✅ **HTML Email Template** - Professional formatted alert emails
✅ **Logging System** - Tracks all emergency alerts
✅ **Multi-recipient Support** - Sends to hundreds of people instantly
✅ **Real-time Feedback** - Shows success/error messages to user

---

## How It Works

1. **User clicks "TRIGGER EMERGENCY ALERT" button on dashboard**
2. **System asks for confirmation** (to prevent accidental triggers)
3. **Button shows "Sending Alerts..." while processing**
4. **Flask backend receives request at `/emergency/trigger` endpoint**
5. **Email function creates professional HTML email**
6. **Sends email to all configured student & staff emails**
7. **Success message shows number of recipients notified**
8. **Alert is logged with timestamp and ID**

---

## 📧 Setup Instructions - CRITICAL STEPS

### Step 1: Get Gmail App Password

1. Go to https://myaccount.google.com/
2. Click **Security** (left sidebar)
3. Find **"App passwords"** section
4. Select **"Mail"** and **"Windows Computer"**
5. Google will generate a 16-character password
6. **Copy this password**

### Step 2: Update Configuration in flask_app.py

Edit the following lines in `flask_app.py` (around line 515-520):

```python
# Line 515
SENDER_EMAIL = "your_email@gmail.com"  # ← Change to YOUR Gmail address

# Line 516
SENDER_PASSWORD = "your_app_password"  # ← Change to the 16-char password from Step 1

# Lines 519-525: Student emails
STUDENT_EMAILS = [
    "student1@campus.edu",  # ← Replace with actual student emails
    "student2@campus.edu",
    # Add all student emails
]

# Lines 527-533: Staff emails
STAFF_EMAILS = [
    "principal@campus.edu",  # ← Replace with actual staff emails
    "security@campus.edu",
    # Add all staff emails
]
```

### Step 3: Add Your Student & Staff Emails

Replace the placeholder emails with actual email addresses:

**Students (Example):**
```python
STUDENT_EMAILS = [
    "student1@university.edu",
    "student2@university.edu",
    "student3@university.edu",
    "student4@university.edu",
    # ... add all students
]
```

**Staff (Example):**
```python
STAFF_EMAILS = [
    "principal@university.edu",
    "security_chief@university.edu",
    "doctor@university.edu",
    "admin@university.edu",
    # ... add all staff
]
```

### Step 4: Restart Flask Server

```bash
# If server is running, stop it (press Ctrl+C)
# Then restart with:
python flask_app.py
```

### Step 5: Test the System

1. Go to http://localhost:5000/
2. Scroll down to "Emergency Alert System" section
3. Click **"TRIGGER EMERGENCY ALERT"** button
4. Click **"OK"** on the confirmation dialog
5. Wait for success message

---

## 📧 Email Details

### What Recipients Receive

When emergency alert is triggered, each student and staff member receives an email with:

```
Subject: 🚨 EMERGENCY ALERT: Campus-Wide Emergency

Email Content:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 EMERGENCY ALERT 🚨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Emergency Type: Campus-Wide Emergency
Location: Campus
Message: An emergency has been triggered. 
         Please move to safe location and await further instructions.

---

Instructions:
1. Move to the nearest safe location immediately
2. Stay calm and follow instructions from campus security
3. Do not leave the premises unless instructed to do so
4. Await further instructions via email or campus announcements

Time: 2026-01-27 18:50:15
Status: ACTIVE INCIDENT
Action Required: Move to safe location
```

---

## 🔧 Troubleshooting

### Problem: "Failed to send emergency alert"

**Solution 1: Check Email Credentials**
- Verify SENDER_EMAIL and SENDER_PASSWORD are correct
- Try logging into Gmail with that account manually

**Solution 2: Use App Password (NOT Regular Password)**
- Regular Gmail password won't work
- Must generate 16-char app password from security settings
- Visit: https://myaccount.google.com/apppasswords

**Solution 3: Enable 2-Step Verification**
- Gmail requires 2-Step Verification to generate app passwords
- Go to: https://myaccount.google.com/security
- Turn ON "2-Step Verification"
- Then generate app password

**Solution 4: Check Recipient List**
- If no emails configured, alert won't send
- Make sure STUDENT_EMAILS and STAFF_EMAILS are not empty

### Problem: "Alert sent but nobody received emails"

**Solution:** Recipients' email servers might be blocking
- Check spam/junk folder
- Contact IT to whitelist sender email

---

## 🔒 Security Notes

⚠️ **IMPORTANT:**
- Don't share the SENDER_PASSWORD with anyone
- Don't commit `flask_app.py` with credentials to public repositories
- Use environment variables for production (optional enhancement)

---

## 📊 Alert Logging

All emergency alerts are automatically logged to `emergency_alerts.json`:

```json
{
  "timestamp": "2026-01-27T18:50:15.123456",
  "type": "Campus-Wide Emergency",
  "location": "Campus",
  "message": "An emergency has been triggered...",
  "recipients_count": 150,
  "status": "SENT"
}
```

---

## 🚀 For Institutional Email (Optional)

If using institutional email instead of Gmail:

1. Contact your IT department for:
   - SMTP server address
   - SMTP port (usually 587)
   - Username and password

2. Update flask_app.py:
```python
SENDER_EMAIL = "alerts@institution.edu"
SENDER_PASSWORD = "institutional_password"
SMTP_SERVER = "mail.institution.edu"  # Ask IT for this
SMTP_PORT = 587  # Confirm with IT
```

---

## ✅ Testing Checklist

- [ ] Gmail app password generated and copied
- [ ] SENDER_EMAIL updated with your Gmail
- [ ] SENDER_PASSWORD updated with 16-char app password
- [ ] Student emails added to STUDENT_EMAILS list
- [ ] Staff emails added to STAFF_EMAILS list
- [ ] Flask server restarted
- [ ] Dashboard loads at http://localhost:5000
- [ ] Emergency button visible on dashboard
- [ ] Test email received successfully
- [ ] Alert shows count of recipients notified
- [ ] Alert logged in emergency_alerts.json

---

## 🎯 Next Steps

1. **Configure email credentials** (Steps 1-2 above)
2. **Add your contact list** (Step 3)
3. **Restart server** (Step 4)
4. **Test the system** (Step 5)
5. **Done!** Emergency alert system is now fully functional

---

## 📞 Support

If you encounter issues:
1. Check the Python terminal output for error messages
2. Check browser console (F12) for JavaScript errors
3. Verify email configuration in flask_app.py
4. Ensure Flask server is running (should see "Running on http://localhost:5000")
5. Test with test email before campus-wide deployment

**Happy to help! 🎉**
