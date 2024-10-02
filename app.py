# app.py
from flask import Flask, request, jsonify
from transformers import pipeline
from sqlalchemy.orm import sessionmaker
from models.user import User, Session
from utils.helpers import analyze_sentiment, get_coping_strategy


app = Flask(__name__)

# Initialize the database session
session = Session()

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

@app.route('/api/mood/<int:user_id>', methods=['POST'])
def mood(user_id):
    data = request.json
    user_input = data.get("message")
    
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
    with open('resources/mindfulness_exercises.txt', 'r') as f:
        exercises = f.readlines()

    # Filter exercises (implement logic based on mood if needed)
    return jsonify({"exercises": exercises})


@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    new_user = User(username=username)
    session.add(new_user)
    session.commit()
    return jsonify({"message": "User created successfully", "user_id": new_user.id})

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return jsonify({"username": user.username, "mood_history": user.mood_history})
    return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)