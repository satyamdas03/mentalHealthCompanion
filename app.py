# app.py
from flask import Flask, request, jsonify
from transformers import pipeline
from utils.helpers import analyze_sentiment

app = Flask(__name__)

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

@app.route('/api/mood', methods=['POST'])
def mood():
    data = request.json
    user_input = data.get("message")
    
    # Perform sentiment analysis
    sentiment_result = analyze_sentiment(user_input)
    
    return jsonify(sentiment_result)

@app.route('/api/exercises', methods=['GET'])
def exercises():
    # Return mindfulness exercises from a file or a predefined list
    with open('resources/mindfulness_exercises.txt', 'r') as f:
        exercises = f.readlines()
    return jsonify(exercises)

if __name__ == '__main__':
    app.run(debug=True)
