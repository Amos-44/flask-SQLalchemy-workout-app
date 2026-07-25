from marshmallow import fields, validate
from config import ma
from models import Exercise, Workout, WorkoutExercise

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True
        include_fk = True

    # Schema Validation 1 & 2
    name = fields.String(
        required=True, 
        validate=validate.Length(min=2, error="Exercise name must be at least 2 characters long.")
    )
    category = fields.String(
        required=True, 
        validate=validate.OneOf(
            ['Cardio', 'Strength', 'Flexibility', 'Balance', 'HIIT'],
            error="Invalid category. Must be one of: Cardio, Strength, Flexibility, Balance, HIIT."
        )
    )
    equipment_needed = fields.Boolean(required=True)


class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True

    # Schema Validation 3
    reps = fields.Integer(validate=validate.Range(min=0, error="Reps must be 0 or greater."))
    sets = fields.Integer(validate=validate.Range(min=0, error="Sets must be 0 or greater."))
    duration_seconds = fields.Integer(validate=validate.Range(min=0, error="Duration in seconds must be 0 or greater."))
    
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True
        include_fk = True

    # Schema Validation 4
    date = fields.Date(required=True, error_messages={"required": "A valid date (YYYY-MM-DD) is required."})
    duration_minutes = fields.Integer(
        required=True, 
        validate=validate.Range(min=1, error="Duration in minutes must be at least 1.")
    )
    notes = fields.String(allow_none=True)

    # Includes sets/reps/duration data in response payload
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)