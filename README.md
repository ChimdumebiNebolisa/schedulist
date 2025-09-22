# 📅 Schedulist

## 🔎 Overview
Schedulist turns the Eisenhower Matrix into a living dashboard so I can sort urgent versus important work without redrawing the grid every day. The app keeps the four quadrants ready, then nudges me toward the tasks that deserve attention first.

The project doubles as a playground for sharpening full-stack habits—automating task workflows, practicing OAuth flows, and shipping a reliable Flask deployment with production-ready polish.

## ✨ Features
- Google OAuth 2.0 sign-in keeps access secure without managing passwords.
- Auto-categorized Eisenhower Matrix board highlights urgent and important tasks at a glance.
- Task CRUD flows with due dates, notes, and completion toggles.
- Responsive Bootstrap styling adapts cleanly to desktops, tablets, and phones.
- PostgreSQL-backed persistence powered by SQLAlchemy models and migrations.
- Filter and focus views to surface today's priorities and upcoming commitments.
- Render-friendly configuration for smooth deployment from development to production.

## 🛠 Tech Stack
- Python 3.11
- Flask + Jinja2
- SQLAlchemy & Flask-Migrate
- PostgreSQL
- Google OAuth 2.0
- Bootstrap 5
- Render hosting

## 🖼 Screenshot
![Schedulist Dashboard](static/img/hero.png)

## ⚙️ Setup Instructions
### Prerequisites
- Python 3.11+
- PostgreSQL instance with a database ready for Schedulist
- Google Cloud project with OAuth credentials (web application type)

### Environment Variables
- `DATABASE_URL`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `FLASK_APP=app.py`

### Local Setup
#### Windows (PowerShell or Command Prompt)
```bat
python -m venv venv
venv\Scripts\activate
set FLASK_APP=app.py
set DATABASE_URL=postgresql://username:password@localhost:5432/schedulist
set GOOGLE_CLIENT_ID=your-google-client-id
set GOOGLE_CLIENT_SECRET=your-google-client-secret
pip install -r requirements.txt
flask db upgrade
flask run
```

#### Linux / macOS (Bash or Zsh)
```bash
python -m venv venv
source venv/bin/activate
export FLASK_APP=app.py
export DATABASE_URL=postgresql://username:password@localhost:5432/schedulist
export GOOGLE_CLIENT_ID=your-google-client-id
export GOOGLE_CLIENT_SECRET=your-google-client-secret
pip install -r requirements.txt
flask db upgrade
flask run
```

## 🧩 Architecture (Optional)
```
[User] → [Flask Routes] → [PostgreSQL]
   ↘
 [Google OAuth]
```
Google OAuth handles identity before users reach the Flask routes, which then orchestrate database interactions. This keeps authentication decoupled from task management logic while maintaining a simple request flow.

## 📚 What I Learned
- Designing around the Eisenhower Matrix clarified how UX choices can nudge better prioritization.
- OAuth integrations demand careful redirect handling and token storage to stay secure.
- SQLAlchemy migrations safeguard data integrity when the model layer evolves.
- Bootstrap utilities speed up responsive layouts without sacrificing customization.
- Automating setup scripts and environment variables reduces onboarding friction for collaborators.

## ✅ Roadmap (Short)
- Add drag-and-drop reordering within quadrants for rapid triage.
- Deliver recurring task reminders and customizable notifications.
- Introduce analytics to surface time spent by quadrant and completion trends.
- Package a lightweight PWA mode for quick mobile access.

## 📜 License
This project is licensed under the terms of the [MIT License](LICENSE).
