# Schedulist

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3110/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)

## Introduction

Schedulist grew out of my habit of sketching the Eisenhower Matrix on paper every morning. Re-creating the quadrants by hand took time away from actually prioritizing, so I decided to build a digital assistant that keeps the grid ready and puts my tasks in the right place automatically. The project runs on a modern stack—Flask paired with SQLAlchemy and PostgreSQL, Google OAuth 2.0 for authentication, and Render for deployment—giving me a playground to refine both backend design and cloud deployment skills.

## Features

- Google login with OAuth-powered authentication
- Eisenhower Matrix dashboard with urgent and important quadrants
- Task creation, editing, and completion flows
- Responsive Bootstrap-powered user interface

## Screenshots

![Schedulist dashboard displaying tasks across the Eisenhower Matrix quadrants](/assets/screenshots/dashboard.png)
<br/><sub>Dashboard view showcasing how urgent/important tasks are separated at a glance.</sub>

## Installation

```bash
git clone https://github.com/your-username/schedulist.git
cd schedulist
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
pip install -r requirements.txt
export DATABASE_URL="postgresql://username:password@localhost:5432/schedulist"
export GOOGLE_CLIENT_ID="your-google-client-id"
export GOOGLE_CLIENT_SECRET="your-google-client-secret"
flask db upgrade
flask run
```

## Usage

Authenticate with your Google account, then add, edit, and complete tasks within the Eisenhower Matrix. Drag urgent items into the top quadrants, park long-term goals in the bottom-right, and mark tasks done as your focus shifts throughout the day.

## Tech Stack

| Layer | Technologies |
| --- | --- |
| Web Framework | ![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white) with SQLAlchemy ORM and Jinja2 templating |
| Database | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white) managed through Flask-Migrate |
| Authentication | ![Google OAuth 2.0](https://img.shields.io/badge/Google%20OAuth%202.0-4285F4?logo=google&logoColor=white) for secure sign-in |
| Hosting | ![Render](https://img.shields.io/badge/Render-46E3B7?logo=render&logoColor=000000) continuous deployment environment |
| Language & Tooling | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) 3.11, ![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white) guarding formatting with Black and linting via Ruff |

## Architecture

```mermaid
flowchart LR
    User --> FlaskRoutes[Flask Routes]
    FlaskRoutes --> Database[(PostgreSQL Database)]
    Database --> GoogleOAuth[Google OAuth 2.0]
    GoogleOAuth --> MatrixView[Matrix View]
    FlaskRoutes --> MatrixView
```

## Roadmap

- Introduce drag-and-drop interactions for rearranging matrix tasks
- Add recurring task scheduling and reminders
- Build analytics to highlight time spent in each quadrant
- Ship a mobile-friendly layout optimized for quick updates
- Automate CI/CD checks with GitHub Actions alongside Render deploys

## Reflection / What I Learned

- Integrating Google OAuth 2.0 demands careful handling of redirect URIs and token refresh to keep sign-in smooth yet secure.
- Flask-Migrate streamlines database changes, but planning migrations early prevents downtime once data is live.
- Deploying to Render reinforced the value of immutable infrastructure and environment-specific configuration.
- pre-commit hooks with Black and Ruff keep the codebase consistent, catching formatting and lint errors before they ship.

## Contributing

Issues and pull requests are welcome. Fork the repository, create feature branches for your updates, and open a pull request describing your changes.

## License

This project is licensed under the [MIT License](LICENSE).
