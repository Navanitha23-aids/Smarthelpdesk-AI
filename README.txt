===============================================
  SMART HELPDESK AI — BACKEND SETUP GUIDE
===============================================

TOOLS USED
----------
- Python        → Backend language
- Flask         → Web framework (runs the server)
- Flask-CORS    → Allows frontend to talk to backend
- SQLite        → Database (saves as helpdesk.db file)

FILES IN THIS FOLDER
--------------------
app.py            → Main backend server (all API routes)
requirements.txt  → List of Python packages to install
login.html        → Updated login (connected to backend)
create.html       → Updated create ticket (connected to backend)
README.txt        → This guide

STEP 1 — INSTALL PYTHON
------------------------
Download Python from: https://www.python.org/downloads/
During install → CHECK the box "Add Python to PATH"

STEP 2 — OPEN TERMINAL IN VS CODE
-----------------------------------
Open VS Code
Press: Ctrl + ` (backtick key)
A terminal opens at the bottom

STEP 3 — INSTALL REQUIRED PACKAGES
-------------------------------------
Type this command and press Enter:

    pip install flask flask-cors

Wait for installation to finish.

STEP 4 — RUN THE BACKEND SERVER
---------------------------------
Type this command and press Enter:

    python app.py

You will see:
    ✅ Tables created successfully!
    🚀 Smart Helpdesk Backend is running!
    🌐 Open: http://127.0.0.1:5000

STEP 5 — OPEN YOUR FRONTEND
------------------------------
Keep the terminal running (do not close it)
Open login.html with Live Server in VS Code

STEP 6 — TEST IT
-----------------
1. Register a new account
2. Login with your email and password
3. Dashboard opens
4. Create a ticket — it saves to database!
5. View tickets in My Tickets page
6. Check history

API ROUTES (for reference)
---------------------------
POST   /api/register         → Create new account
POST   /api/login            → Login
POST   /api/tickets          → Create ticket
GET    /api/tickets          → Get all tickets
GET    /api/tickets/<id>     → Get one ticket
PUT    /api/tickets/<id>     → Update ticket status
DELETE /api/tickets/<id>     → Delete ticket
GET    /api/stats            → Dashboard counts
GET    /api/history          → Full history

DATABASE
--------
A file called helpdesk.db will be created automatically
when you run app.py for the first time.
You can open it with: DB Browser for SQLite (free tool)
Download: https://sqlitebrowser.org/

===============================================
