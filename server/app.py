from flask import request, jsonify, make_response
from marshmallow import ValidationError
from config import create_app, db
from models import Exercise, Workout, WorkoutExercise
from schemas import (
    workout_schema, workouts_schema,
    exercise_schema, exercises_schema,
    workout_exercise_schema
)

app = create_app()

@app.route('/')
def index():
    """Welcome route providing API information and available endpoints."""
    return make_response(jsonify({
        "message": "Welcome to the Workout Application Backend API! ",
        "endpoints": {
            "workouts": "/workouts",
            "exercises": "/exercises"
        }
    }), 200)

# WORKOUT ROUTES 

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.jsonify(workouts), 200)

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    return make_response(workout_schema.jsonify(workout), 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        new_workout = workout_schema.load(json_data, session=db.session)
        db.session.add(new_workout)
        db.session.commit()
        return make_response(workout_schema.jsonify(new_workout), 201)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 422)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": "Workout successfully deleted"}), 200)

# EXERCISE ROUTES

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.jsonify(exercises), 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    return make_response(exercise_schema.jsonify(exercise), 200)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)

    try:
        new_exercise = exercise_schema.load(json_data, session=db.session)
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(exercise_schema.jsonify(new_exercise), 201)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 422)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": "Exercise successfully deleted"}), 200)

# JOIN TABLE ROUTE 

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    json_data = request.get_json() or {}
    json_data['workout_id'] = workout_id
    json_data['exercise_id'] = exercise_id

    try:
        new_workout_exercise = workout_exercise_schema.load(json_data, session=db.session)
        db.session.add(new_workout_exercise)
        db.session.commit()
        return make_response(workout_exercise_schema.jsonify(new_workout_exercise), 201)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 422)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

    