from flask import Flask, request, jsonify, render_template  # Import render_template
from transformers import pipeline
from sqlalchemy.orm import sessionmaker
from models.user import User, Session
from utils.helpers import analyze_sentiment, get_coping_strategy
from flask_httpauth import HTTPBasicAuth
from flask_swagger_ui import get_swaggerui_blueprint
import json  # Import json module

# Initialize the Flask app
app = Flask(__name__)

# Swagger setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Create this JSON file for your API

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mental Health Companion"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

auth = HTTPBasicAuth()

# users = {
#     "admin": "password"
# }

# Initialize the database session
session = Session()

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


# @auth.verify_password
# def verify_password(username, password):
#     if username in users and users[username] == password:
#         return username
#     return None

@app.route('/')
def home():
    return render_template('index.html')  # Render the index.html template

@app.route('/api/mood/<int:user_id>', methods=['POST'])
def mood(user_id):
    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Message is required."}), 400
    
    # Perform sentiment analysis
    sentiment_result = analyze_sentiment(user_input)
    coping_strategy = get_coping_strategy(sentiment_result['label'])
    
    # Update user mood history
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        if user.mood_history:
            user.mood_history += f"; {sentiment_result['label']}"
        else:
            user.mood_history = sentiment_result['label']
        session.commit()
    else:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "sentiment": sentiment_result,
        "coping_strategy": coping_strategy
    })

@app.route('/api/exercises/<int:user_id>', methods=['GET'])
def exercises(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    mood = user.mood_history.split(";")[-1] if user.mood_history else "NEUTRAL"

    # Load exercises based on mood
    with open('resources/exercises.json', 'r') as f:
        exercises = json.load(f)

    return jsonify({"exercises": exercises.get(mood, ["No exercises available."])})

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if the user already exists
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=username, password=password)  # Assuming User model has password field
    session.add(new_user)
    session.commit()
    return jsonify({"message": "User created successfully", "user_id": new_user.id})

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        return jsonify({"message": "Login successful", "user_id": user.id})
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return jsonify({"username": user.username, "mood_history": user.mood_history})
    return jsonify({"error": "User not found"}), 404

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.json
    user_id = data.get('user_id')
    feedback_text = data.get('feedback')

    # Save feedback logic (e.g., to a file or database)
    
    return jsonify({"message": "Feedback received!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
