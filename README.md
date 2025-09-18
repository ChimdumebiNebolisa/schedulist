# Schedulist

Schedulist is a task management web app built with Flask, SQLAlchemy, and Google OAuth, deployed on Render with PostgreSQL.

## Features

- Google login with OAuth-powered authentication
- Eisenhower Matrix dashboard with urgent and important quadrants
- Task creation, editing, and completion flows
- Responsive Bootstrap-powered user interface

## Screenshots

![Schedulist dashboard showing urgent and not-urgent quadrants](/assets/dashboard.png)
<br/><sub>Dashboard view highlighting urgent vs. not-urgent task quadrants.</sub>

## Local Development

1. Clone the repository and navigate into the project directory.
2. Create and activate a Python 3.11+ virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Export required environment variables:
   ```bash
   export DATABASE_URL=...
   export GOOGLE_CLIENT_ID=...
   export GOOGLE_CLIENT_SECRET=...
   ```
5. Apply database migrations with `flask db upgrade`.
6. Start the development server with `flask run`.

## Deployment

Pushing to the main branch on GitHub triggers an automatic deploy on Render, where the gunicorn start command is already configured.

## Contributing

Issues and pull requests are welcome. Fork the repository, create feature branches for your updates, and open a pull request describing your changes.

## License

This project is licensed under the [MIT License](LICENSE).
