# 🚀 QUICK SETUP - 5 MINUTES

## Current Status
✅ Emergency alert button is NOW FUNCTIONAL
✅ Email system is ready to use
⏳ Just need your Gmail credentials

---

## 3 Easy Steps

### 1️⃣ Get Gmail App Password (2 min)
```
1. Go to https://myaccount.google.com/
2. Click "Security"
3. Click "App passwords"
4. Choose "Mail" → "Windows Computer"
5. Copy the 16-character password
```

### 2️⃣ Edit flask_app.py (2 min)

Find these lines (around line 515-533):

**BEFORE:**
```python
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
STUDENT_EMAILS = [
    "student1@campus.edu",
    "student2@campus.edu",
]
STAFF_EMAILS = [
    "staff1@campus.edu",
    "principal@campus.edu",
]
```

**AFTER (your values):**
```python
SENDER_EMAIL = "myemail@gmail.com"  # Your Gmail address
SENDER_PASSWORD = "abcd efgh ijkl mnop"  # 16-char from Step 1
STUDENT_EMAILS = [
    "alice@university.edu",
    "bob@university.edu",
    "charlie@university.edu",
    # ... all students
]
STAFF_EMAILS = [
    "principal@university.edu",
    "security@university.edu",
    "doctor@university.edu",
    # ... all staff
]
```

### 3️⃣ Restart Flask (1 min)
```bash
# Stop the running server (Ctrl+C)
# Start it again:
python flask_app.py
```

---

## 🧪 Test It

1. Go to http://localhost:5000
2. Scroll to "Emergency Alert System"
3. Click **"TRIGGER EMERGENCY ALERT"**
4. Click **"OK"** to confirm
5. ✅ See "Alert sent to X recipients"
6. 📧 Check if recipients got the email

---

## 🎉 Done!

Your emergency alert system is now LIVE and will:
- ✅ Send emails instantly when alert is triggered
- ✅ Notify all students and staff automatically
- ✅ Log each alert with timestamp and ID
- ✅ Show success/error messages to user
- ✅ Work 24/7 on campus network

---

## If it doesn't work:

**Check 1:** Are STUDENT_EMAILS and STAFF_EMAILS filled with real addresses?
**Check 2:** Did you use the 16-char APP PASSWORD (not regular Gmail password)?
**Check 3:** Is Flask server running? (should say "Running on http://localhost:5000")
**Check 4:** Check Python output for error messages

---

**Need help?** See EMERGENCY_ALERT_SETUP.md for detailed troubleshooting
