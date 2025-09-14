# Schedulist

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

Schedulist is a work-in-progress productivity tool designed to help organize and prioritize tasks.

## Installation

1. Clone this repository.
2. Navigate into the project directory.
3. Copy `.env.example` to `.env` and replace the placeholder values with your Google Cloud credentials and database connection string.

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the development server:
   ```bash
   flask --app app run
   ```
   This command explicitly references the app module and works without extra environment variables. If you prefer the shorter `flask run`, first set `FLASK_APP=app`.

   macOS/Linux
   ```bash
   export FLASK_APP=app
   flask run
   ```

   Windows (PowerShell)
   ```powershell
   $env:FLASK_APP="app"
   flask run
   ```

   Windows (cmd.exe)
   ```cmd
   set FLASK_APP=app
   flask run
   ```

## Database Setup

The application reads its database connection string from the
`DATABASE_URL` environment variable. Provide a PostgreSQL URL such as:

```bash
export DATABASE_URL="postgresql://user:password@localhost/schedulist"
```

If `DATABASE_URL` is not set, the app falls back to a local SQLite file
(`schedulist.db`). Running the server as shown above initializes the database
and generates the SQLite file. You can also run the module directly:

```bash
python app.py
```

## Usage

Start the application with:

```bash
flask --app app run
```

Running `python app.py` directly will also start the development server. With
the server running, visit `http://127.0.0.1:5000/add` to create a new
task and view it in the matrix on the home page.

Usage will expand as features are implemented.

## Google OAuth Setup

To try logging in with Google, copy `.env.example` to `.env` and fill in:

- `SECRET_KEY` – session secret for Flask
- `GOOGLE_CLIENT_ID` – OAuth client ID from Google Cloud Console
- `GOOGLE_CLIENT_SECRET` – matching client secret
- `DATABASE_URL` – PostgreSQL connection string for the app (optional)

The application loads these values automatically using [python-dotenv](https://saurabh-kumar.com/python-dotenv). After
the file is created, navigate to `/login` to initiate the OAuth flow.

## Deployment

Schedulist is deployed on Render at:

https://schedulist.onrender.com

To deploy your own instance on [Render](https://render.com):

1. Create a new **Web Service** and point it at this repository.
2. Choose a Python environment and set the start command:
   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```
3. Configure the required environment variables:
   - `SECRET_KEY` – session secret for Flask
   - `GOOGLE_CLIENT_ID` – OAuth client ID from Google Cloud Console
   - `GOOGLE_CLIENT_SECRET` – matching client secret
4. Trigger a deploy. Render will build the service and expose it at a `.onrender.com` URL.

## Planned Features

- Web interface built with [Flask](https://flask.palletsprojects.com/)
- Task prioritization using the [Eisenhower Matrix](https://en.wikipedia.org/wiki/Time_management#The_Eisenhower_Method)
- Additional productivity enhancements

Contributions and feedback are welcome.
