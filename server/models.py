from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from config import db

class Exercise(db.Model):
    __tablename__ = 'exercises'

    # Table Constraint 1: Minimum name length check
    __table_args__ = (
        CheckConstraint('length(name) >= 2', name='check_exercise_name_length'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # Cascade delete removes join table records automatically
    workout_exercises = db.relationship(
        'WorkoutExercise', 
        back_populates='exercise', 
        cascade='all, delete-orphan'
    )
    workouts = db.relationship(
        'Workout', 
        secondary='workout_exercises', 
        back_populates='exercises',
        viewonly=True
    )

    # Model Validation 1
    @validates('name')
    def validate_name(self, key, name):
        if not name or not isinstance(name, str) or len(name.strip()) < 2:
            raise ValueError("Exercise name must be a string at least 2 characters long.")
        return name.strip()

    # Model Validation 2
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Cardio', 'Strength', 'Flexibility', 'Balance', 'HIIT']
        if category not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category

    def __repr__(self):
        return f"<Exercise id={self.id} name='{self.name}' category='{self.category}'>"


class Workout(db.Model):
    __tablename__ = 'workouts'

    # Table Constraint 2: Duration must be positive
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_workout_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    # Cascade delete removes join table records automatically
    workout_exercises = db.relationship(
        'WorkoutExercise', 
        back_populates='workout', 
        cascade='all, delete-orphan'
    )
    exercises = db.relationship(
        'Exercise', 
        secondary='workout_exercises', 
        back_populates='workouts',
        viewonly=True
    )

    # Model Validation 3
    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is None or not isinstance(duration, int) or duration <= 0:
            raise ValueError("Workout duration must be a positive integer greater than 0.")
        return duration

    def __repr__(self):
        return f"<Workout id={self.id} date='{self.date}' duration={self.duration_minutes}m>"


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # Model Validation 4
    @validates('reps', 'sets', 'duration_seconds')
    def validate_metrics(self, key, value):
        if value is not None:
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"{key.capitalize()} must be a non-negative integer.")
        return value

    def __repr__(self):
        return f"<WorkoutExercise id={self.id} workout_id={self.workout_id} exercise_id={self.exercise_id}>"