# 📦 Hostel Manager Project Setup Guide

## 📁 Folder Structure
```
AI-Powered Hostel-Manager/
│
├── backend/                     # Flask backend app
│   ├── app.py                  # Main Flask app entry point
│   ├── config.py               # Configurations (DB, API keys, etc.)
│   ├── requirements.txt        # Python dependencies
│   ├── models/                 # ML models and related scripts
│   │    ├── room_recommendation.py
│   │    ├── anomaly_detection.py
│   │    ├── complaint_priority.py
│   │    ├── mess_forecast.py
│   │    └── stay_duration.py
│   ├── routes/                 # Flask route handlers (blueprints)
│   │    ├── auth.py            # Student registration, login APIs
│   │    ├── rooms.py           # Room allocation APIs
│   │    ├── mess.py            # Mess management APIs
│   │    ├── complaints.py      # Complaint handling APIs
│   │    ├── admin.py           # Admin dashboard routes
│   │    └── notifications.py   # Alerts and notifications routes
│   ├── services/               # Business logic, ML integration, helpers
│   │    └── ml_service.py
│   ├── static/                 # Backend static files (optional)
│   ├── templates/              # Jinja2 templates if using Flask for frontend (optional)
│   └── utils.py                # Utility functions
│
├── frontend/                   # Frontend files served separately or via Flask
│   ├── index.html              # Main landing page
│   ├── css/                   
│   │    └── styles.css         # All CSS files
│   ├── js/
│   │    ├── main.js            # Main JS file (fetch APIs, DOM manipulation)
│   │    ├── roomAllocation.js
│   │    ├── messManagement.js
│   │    └── complaintHandling.js
│   ├── assets/                 # Images, icons, fonts, etc.
│   └── components/             # Optional if you go React or modular JS
│
├── database/                   # DB schema, migration scripts, seed data
│   ├── schema.sql
│   ├── seeds.sql
│   └── migrations/             # Alembic or other migration tools
│
├── ml_models/                  # Serialized/trained ML models saved here (.pkl files)
│   ├── room_recommendation.pkl
│   ├── anomaly_detection.pkl
│   ├── complaint_priority.pkl
│   ├── mess_forecast.pkl
│   └── stay_duration.pkl
│
├── tests/                      # Unit and integration tests (backend & frontend)
│   ├── backend/
│   └── frontend/
│
├── docs/                       # Documentation, API specs, project proposal, etc.
│
├── .gitignore                  # Git ignore file
├── README.md                   # Project overview & setup instructions
└── run.sh / run.bat            # Optional scripts to start your Flask server

```

## ✅ How to Run
1. Place this entire project folder in your local system.
2. Open `index.html` in your browser to begin.
3. All data is fetched from local JSON files (no backend needed).
4. Use Postman or browser tools to inspect and simulate data calls.

## 📌 Features Included
- Student Registration
- Room Allocation
- Mess Menu and Attendance
- Complaint Management
- Admin Data Export Panel

> All pages are interactive, styled, and simulate real backend APIs using JSON & JavaScript.

## 📢 Notes
- This project is completely frontend-based (HTML/CSS/JS/JSON).
- You can import JSON into Postman for mock API testing.

Happy Coding! 💻
