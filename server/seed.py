#!/usr/bin/env python3

from datetime import date
from config import db, create_app
from models import Exercise, Workout, WorkoutExercise

app = create_app()

def seed_database():
    with app.app_context():
        print("Clearing existing database tables...")
        WorkoutExercise.query.delete()
        Exercise.query.delete()
        Workout.query.delete()
        db.session.commit()

        print("Creating seed exercises...")
        e1 = Exercise(name="Push-ups", category="Strength", equipment_needed=False)
        e2 = Exercise(name="Treadmill Run", category="Cardio", equipment_needed=True)
        e3 = Exercise(name="Bodyweight Squats", category="Strength", equipment_needed=False)
        e4 = Exercise(name="Plank", category="Balance", equipment_needed=False)

        db.session.add_all([e1, e2, e3, e4])
        db.session.commit()

        print("Creating seed workouts...")
        w1 = Workout(date=date(2026, 3, 15), duration_minutes=45, notes="Upper body and core focus.")
        w2 = Workout(date=date(2026, 3, 16), duration_minutes=30, notes="Light cardio morning session.")

        db.session.add_all([w1, w2])
        db.session.commit()

        print("Creating seed workout exercises...")
        we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, reps=15, sets=4, duration_seconds=None)
        we2 = WorkoutExercise(workout_id=w1.id, exercise_id=e4.id, reps=None, sets=3, duration_seconds=60)
        we3 = WorkoutExercise(workout_id=w2.id, exercise_id=e2.id, reps=None, sets=1, duration_seconds=1800)

        db.session.add_all([we1, we2, we3])
        db.session.commit()

        print("Database successfully seeded.")

if __name__ == '__main__':
    seed_database()