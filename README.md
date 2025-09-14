# Schedulist

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

Schedulist is a work-in-progress productivity tool designed to help organize and prioritize tasks.

## Installation

1. Clone this repository.
2. Navigate into the project directory.
3. Copy `.env.example` to `.env` and replace the placeholder values with your
   Google Cloud credentials.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the development server:
   ```bash
   flask --app app run
   ```

## Database Setup

The application reads its database connection string from the
`DATABASE_URL` environment variable. Provide a PostgreSQL URL such as:

```bash
export DATABASE_URL="postgresql://user:password@localhost/schedulist"
```

If `DATABASE_URL` is not set, the app falls back to a local SQLite file
(`schedulist.db`). To initialize the database manually, run:

```bash
python app.py
# or
flask --app app run
```

This will generate a `schedulist.db` file in the project directory with the
required tables.

If you prefer to rely on the Flask CLI's default discovery, set the
`FLASK_APP` environment variable before running `flask run`:

```bash

export FLASK_APP=app   # macOS/Linux
flask run
```

On Windows:

```powershell
$env:FLASK_APP="app"   # PowerShell
flask run

:: or using cmd.exe
set FLASK_APP=app
flask run
```

## Usage

After installing the dependencies, the application can be started locally once the Flask app is ready:

```bash
python app.py
# or
flask --app app run
```

To use the default `flask run` command without `--app`, make sure
`FLASK_APP` is set as shown above.


With the server running, visit `http://127.0.0.1:5000/add` to create a new
task and view it in the matrix on the home page.

Usage will expand as features are implemented.

## Google OAuth Setup

To try logging in with Google, copy `.env.example` to `.env` and fill in:

- `SECRET_KEY` – session secret for Flask
- `GOOGLE_CLIENT_ID` – OAuth client ID from Google Cloud Console
- `GOOGLE_CLIENT_SECRET` – matching client secret

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
