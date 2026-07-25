# Workout Application Backend API

A RESTful backend API built with **Flask**, **Flask-SQLAlchemy**, and **Marshmallow** for managing workouts and exercises. The application allows users to create workouts, manage exercises, and associate exercises with workouts using a many-to-many relationship.

---

# Overview

This project demonstrates backend development using Flask and SQLAlchemy by implementing a fully functional RESTful API. It supports CRUD operations, database relationships, serialization with Marshmallow, input validation, and database migrations with Flask-Migrate.

The API enables users to:

- Create and manage workouts
- Create and manage exercises
- Associate exercises with workouts
- Track workout metrics such as sets, reps, and duration
- Validate incoming data before storing it in the database
- Seed the database with sample data

---

# Project Structure

```
workout-app-backend/
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── README.md
└── server/
    ├── app.py
    ├── config.py
    ├── models.py
    ├── schemas.py
    ├── seed.py
    └── migrations/
```

> **All commands (`git`, `pipenv`, `flask`, and `python`) should be run from the project root directory, NOT inside the `server/` folder.**

---

# Setup and Installation

## 1. Clone the repository

```bash
git clone <repository_url>
cd flask-SQLalchemy-workout-app
```

---

## 2. Install dependencies

```bash
pipenv install
```

> **Note:** If you receive `Warning: Python 3.8 was not found`, open the `Pipfile` and change:

```toml
python_version = "3.8"
```

to match your installed Python version (for example `"3.12"`), then run:

```bash
pipenv install
```

again.

---

## 3. Set the Flask application path

### Linux / macOS

```bash
export FLASK_APP=server/app.py
```

### Windows (Command Prompt)

```cmd
set FLASK_APP=server/app.py
```

### Windows (PowerShell)

```powershell
$env:FLASK_APP="server/app.py"
```

> **This environment variable must be set before running any Flask migration commands.**

---

## 4. Initialize and migrate the database

### Option A — Using `pipenv run`

```bash
pipenv run flask db init
pipenv run flask db migrate -m "Initial migration"
pipenv run flask db upgrade head
```

### Option B — Using the Pipenv shell

```bash
pipenv shell
flask db init
flask db migrate -m "Initial migration"
flask db upgrade head
```

> **Do not run `flask` directly unless you are inside the Pipenv shell or using `pipenv run`. Otherwise, you may encounter `Command 'flask' not found`.**

---

## 5. Seed the database

### Option A — Using `pipenv run`

```bash
pipenv run python server/seed.py
```

### Option B — Using the Pipenv shell

```bash
pipenv shell
python server/seed.py
```

> **Always run Python through Pipenv to ensure the correct virtual environment is used.**

---

# Running the Application

### Option A — Using `pipenv run`

```bash
pipenv run python server/app.py
```

### Option B — Using the Pipenv shell

```bash
pipenv shell
python server/app.py
```

The API will start at:

```
http://localhost:5555
```

---

# API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | Retrieve all workouts. |
| GET | `/workouts/<id>` | Retrieve a specific workout together with its associated exercises and metrics. |
| POST | `/workouts` | Create a new workout. |
| DELETE | `/workouts/<id>` | Delete a workout and all related workout-exercise records. |
| GET | `/exercises` | Retrieve all exercises. |
| GET | `/exercises/<id>` | Retrieve a specific exercise together with its associated workouts. |
| POST | `/exercises` | Create a new exercise. |
| DELETE | `/exercises/<id>` | Delete an exercise and its related workout records. |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Assign an exercise to a workout with sets, reps, or duration information. |

---

# Database Models

## Exercise

Represents an exercise that can be included in one or more workouts.

**Attributes**

- id
- name
- category
- equipment_needed

---

## Workout

Represents a workout session.

**Attributes**

- id
- date
- duration_minutes
- notes

---

## WorkoutExercise

Join table linking workouts and exercises while storing workout-specific exercise metrics.

**Attributes**

- id
- workout_id
- exercise_id
- reps
- sets
- duration_seconds

---

# Validations & Constraints

## Database Constraints

- `CheckConstraint('length(name) >= 2')` on the **Exercise** table.
- `CheckConstraint('duration_minutes > 0')` on the **Workout** table.

## Model Validations

- Exercise category must be one of:
  - Cardio
  - Strength
  - Flexibility
  - Balance
  - HIIT
- Workout duration must be a positive integer greater than zero.
- WorkoutExercise metrics (`reps`, `sets`, and `duration_seconds`) must be non-negative integers.

## Schema Validations

Marshmallow validates incoming request data before it is saved to the database.

Invalid requests return:

- **HTTP 422 – Unprocessable Entity**
- Structured validation error messages describing the validation failure.

---

# Technologies Used

- Python
- Flask
- Flask SQLAlchemy
- Flask Migrate
- Marshmallow
- SQLite
- Pipenv

---

# Author

**Amos Kiplangat**
