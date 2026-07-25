from config import create_app, db
from models import Exercise, Workout, WorkoutExercise

# Initialize the Flask application
app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)