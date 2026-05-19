# Advanced-Employee-Management-System
## 🚀 How to Run the Project

Aap is project ko do tarike se run kar sakte hain: direct Executable (`.exe`) file ke zariye ya fir Python source code ke zariye.

### Prerequisites (Zaroori Cheezein)
Is project ko chalane ke liye aapke system mein niche di gayi cheezein honi chahiye:
1. **Oracle Database Express Edition (XE):** Aapke system mein Oracle local server (localhost:1521) run ho raha ho.
2. **Database Credentials:** Default configuration ke mutabik SQL script run honi chahiye aur database ka password `Kh$074571` set hona chahiye (ya aap `main.py` mein connection string ko apne mutabik update kar sakte hain).

---

### Method 1: Direct Run using Executable (.exe) — Recommended for Quick Testing
Agar aap bina Python install kiye project chalana chahte hain:
1. Repository se `EmployeeManagementSystem.exe` file ko download karein.
2. Apne Oracle Database server ko start karein.
3. `.exe` file par double-click karke application ko run karein.

---

### Method 2: Run via Python Source Code (Development Mode)

Agar aap code ko run ya modify karna chahte hain, toh in steps ko follow karein:

#### Step 1: Python Install Karein
Yaqeen karlein ke aapke system mein **Python 3.x** installed hai.

#### Step 2: Required Libraries Install Karein
Terminal ya Command Prompt open karein aur Oracle database connectivity ke liye `oracledb` library install karein:
```bash
pip install oracledb
