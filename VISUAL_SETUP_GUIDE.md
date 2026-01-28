# 🎯 Exact Changes Needed - Visual Guide

## Where to Make Changes

### File: `flask_app.py`

#### Location 1: Line 515 - Email Address
```python
# BEFORE:
SENDER_EMAIL = "your_email@gmail.com"

# AFTER (Your Gmail):
SENDER_EMAIL = "myactualname@gmail.com"

# EXAMPLE:
SENDER_EMAIL = "vaishnavi.gandewar@gmail.com"
```

---

#### Location 2: Line 516 - App Password
```python
# BEFORE:
SENDER_PASSWORD = "your_app_password"

# AFTER (16-character password):
SENDER_PASSWORD = "abcd efgh ijkl mnop"

# ACTUAL EXAMPLE:
SENDER_PASSWORD = "xyzA bcde fGhi jKlm"
```

⚠️ **Important:** This MUST be the 16-character app password from Gmail
NOT your regular Gmail password!

---

#### Location 3: Lines 519-525 - Student Emails
```python
# BEFORE:
STUDENT_EMAILS = [
    "student1@campus.edu",
    "student2@campus.edu",
    "student3@campus.edu",
    # Add more student emails
]

# AFTER (Your actual students):
STUDENT_EMAILS = [
    "alice.johnson@university.edu",
    "bob.smith@university.edu",
    "charlie.brown@university.edu",
    "diana.prince@university.edu",
    "emma.watson@university.edu",
    "frank.castle@university.edu",
    "grace.hopper@university.edu",
    "henry.ford@university.edu",
    # Add more student emails
]
```

📌 **Add as many as needed** - System handles 100+ emails easily

---

#### Location 4: Lines 527-533 - Staff Emails
```python
# BEFORE:
STAFF_EMAILS = [
    "staff1@campus.edu",
    "staff2@campus.edu",
    "principal@campus.edu",
    "security@campus.edu",
    # Add more staff emails
]

# AFTER (Your actual staff):
STAFF_EMAILS = [
    "principal.sharma@university.edu",
    "security.chief@university.edu",
    "doctor.patel@university.edu",
    "admin.office@university.edu",
    "dean.sharma@university.edu",
    "registrar@university.edu",
    "director.operations@university.edu",
    "security.guard1@university.edu",
    "security.guard2@university.edu",
    # Add more staff emails
]
```

📌 **Include all staff** - Principal, security, medical, admin, etc.

---

## How to Edit the File

### Method 1: Using VS Code (Recommended)

1. **Open Flask App File**
   - Open VS Code
   - Click File → Open File
   - Navigate to `flask_app.py`
   - Click Open

2. **Go to Line 515**
   - Press `Ctrl + G`
   - Type `515`
   - Press Enter

3. **Make Changes**
   - Find the 4 sections above
   - Replace with your values
   - Save file (`Ctrl + S`)

### Method 2: Using Find & Replace

1. **Press `Ctrl + H`** to open Find & Replace
2. **Find:** `"your_email@gmail.com"`
3. **Replace:** `"your_gmail@gmail.com"`
4. **Find:** `"your_app_password"`
5. **Replace:** `"your_16_char_app_password"`
6. **Find:** `"student1@campus.edu"`
7. **Replace:** Your actual student emails
8. **Find:** `"staff1@campus.edu"`
9. **Replace:** Your actual staff emails

### Method 3: Using Text Editor

1. Right-click `flask_app.py`
2. Open with Notepad (or your editor)
3. Use `Ctrl + F` to find sections
4. Replace values
5. Save file

---

## Step-by-Step Visual Example

### Your flask_app.py before:
```python
515  SENDER_EMAIL = "your_email@gmail.com"
516  SENDER_PASSWORD = "your_app_password"
517  SMTP_SERVER = "smtp.gmail.com"
518  SMTP_PORT = 587
519  
520  STUDENT_EMAILS = [
521      "student1@campus.edu",
522      "student2@campus.edu",
523      "student3@campus.edu",
524      # Add more student emails
525  ]
526  
527  STAFF_EMAILS = [
528      "staff1@campus.edu",
529      "staff2@campus.edu",
530      "principal@campus.edu",
531      "security@campus.edu",
532      # Add more staff emails
533  ]
```

### Your flask_app.py after:
```python
515  SENDER_EMAIL = "vaishnavi.gandewar@gmail.com"
516  SENDER_PASSWORD = "xyza bcde fghi jklm"
517  SMTP_SERVER = "smtp.gmail.com"
518  SMTP_PORT = 587
519  
520  STUDENT_EMAILS = [
521      "student1@myuniversity.edu",
522      "student2@myuniversity.edu",
523      "student3@myuniversity.edu",
524      "student4@myuniversity.edu",
525      "student5@myuniversity.edu",
526  ]
527  
528  STAFF_EMAILS = [
529      "principal@myuniversity.edu",
530      "security.chief@myuniversity.edu",
531      "medical@myuniversity.edu",
532      "admin@myuniversity.edu",
533  ]
```

---

## Getting Your Gmail App Password (Visual)

### Step 1: Visit Gmail Security
```
Open: https://myaccount.google.com/
You'll see a page like this:

┌────────────────────────────────┐
│  Google Account                │
│  ├─ Personal info              │
│  ├─ Security  ← CLICK HERE     │
│  ├─ Privacy                    │
│  └─ More...                    │
└────────────────────────────────┘
```

### Step 2: Find App Passwords
```
On Security page, scroll down until you find:

┌────────────────────────────────┐
│  2-Step Verification           │
│  ✅ (enabled)                  │
│                                │
│  App passwords  ← CLICK HERE   │
│  (for less secure apps)        │
└────────────────────────────────┘
```

### Step 3: Generate Password
```
Click "App passwords"

Select: Mail ▼
        Windows Computer ▼

Google shows:

┌────────────────────────────────┐
│  Your app password:            │
│  ┌────────────────────────────┐│
│  │ xyza bcde fghi jklm        ││
│  └────────────────────────────┘│
│                                │
│  [COPY BUTTON]                 │
└────────────────────────────────┘
```

### Step 4: Copy & Paste
```
1. Click the 16-character password
2. It copies to clipboard
3. Paste into flask_app.py line 516:
   SENDER_PASSWORD = "xyza bcde fghi jklm"
```

---

## Verification Checklist

After making changes:

- [ ] Line 515: Email is your actual Gmail (example@gmail.com)
- [ ] Line 516: Password is 16 characters with spaces
- [ ] Lines 520-525: Has multiple real student emails
- [ ] Lines 528-533: Has multiple real staff emails
- [ ] No more placeholder text (your_email, student1, etc.)
- [ ] File saved (Ctrl + S)
- [ ] Flask server restarted

---

## Common Mistakes to Avoid

❌ **Wrong:** Using regular Gmail password instead of app password
✅ **Right:** Use the 16-character app password from security settings

❌ **Wrong:** Using old email addresses
✅ **Right:** Use current, active email addresses

❌ **Wrong:** Leaving placeholder text like "student1@campus.edu"
✅ **Right:** Replace with actual real emails

❌ **Wrong:** Forgetting to save the file
✅ **Right:** Press Ctrl+S after making changes

❌ **Wrong:** Not restarting Flask after changes
✅ **Right:** Stop server (Ctrl+C), then run: python flask_app.py

---

## Verification After Changes

### Check 1: File is Saved
- Look at tab name in VS Code
- Should NOT have a dot (•) indicating unsaved changes

### Check 2: Values Look Correct
- Email should be actual Gmail
- Password should be 16 characters
- Emails should be real addresses (not placeholders)

### Check 3: Server Restarts
- Stop old server (Ctrl+C)
- Run new server: `python flask_app.py`
- Should see: "Running on http://127.0.0.1:5000"

### Check 4: Test the System
- Go to http://localhost:5000
- Click emergency button
- Should show success message
- Recipients should get email

---

## If You Get an Error

### Error: "SMTP authentication failed"
→ Check SENDER_PASSWORD is 16-character app password (not regular password)

### Error: "Connection refused"
→ Flask server isn't running; type: `python flask_app.py`

### Error: "No recipients"
→ Make sure STUDENT_EMAILS and STAFF_EMAILS lists are not empty

### Error: "Invalid email address"
→ Check for typos in email addresses (use @ symbol, no spaces)

---

## Need Help?

Check these files in order:
1. **QUICK_START_ALERT.md** - 5-minute guide
2. **EMERGENCY_ALERT_SETUP.md** - Detailed setup guide
3. **EMERGENCY_SYSTEM_COMPLETE.md** - Full documentation
4. **This file (VISUAL_SETUP_GUIDE.md)** - What you're reading now

---

## Summary

### What to Edit:
- File: `flask_app.py`
- Lines: 515-533

### What to Change:
- Line 515: Your Gmail email
- Line 516: 16-char app password
- Lines 520-525: Student email list
- Lines 528-533: Staff email list

### How Long:
- Getting password: 2 minutes
- Making changes: 2 minutes
- Restarting server: 1 minute
- **Total: 5 minutes** ⏱️

### Then:
✅ Test the emergency button
✅ Verify emails work
✅ Done! System is live 🎉

---

**Ready? Start with getting your Gmail app password!**
