from flask import Flask
from flask_cors import CORS
from config import FRONTEND_ORIGIN
from routes.meals import meals_bp
from routes.goals import goals_bp

app = Flask(__name__)

CORS(
    app,
    origins=[FRONTEND_ORIGIN],
    allow_headers=["Authorization", "Content-Type"],
    methods=["GET", "POST", "OPTIONS"],
)

app.register_blueprint(meals_bp)
app.register_blueprint(goals_bp)

if __name__ == "__main__":
    app.run(debug=True)
