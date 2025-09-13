# Schedulist

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

Schedulist is a work-in-progress productivity tool designed to help organize and prioritize tasks.

## Installation

1. Clone this repository.
2. Navigate into the project directory.
3. Install dependencies (once available). For example:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

This project uses a SQLite database. The database file is created
automatically when the application starts. To initialize the database
manually, run:

```bash
flask run
```

This will generate a `schedulist.db` file in the project directory with the
required tables.

## Usage

After installing the dependencies, the application can be started locally once the Flask app is ready:

```bash
flask run
```

Usage will expand as features are implemented.

## Planned Features

- Web interface built with [Flask](https://flask.palletsprojects.com/)
- Task prioritization using the [Eisenhower Matrix](https://en.wikipedia.org/wiki/Time_management#The_Eisenhower_Method)
- Additional productivity enhancements

Contributions and feedback are welcome.
