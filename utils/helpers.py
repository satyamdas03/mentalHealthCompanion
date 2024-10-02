# utils/helpers.py
from transformers import pipeline
import random

def analyze_sentiment(text):
    sentiment_analyzer = pipeline("sentiment-analysis")
    result = sentiment_analyzer(text)
    return {
        "label": result[0]['label'],
        "score": result[0]['score']
    }


def get_coping_strategy(sentiment):
    strategies = {
        "POSITIVE": [
            "Keep up the good work! Consider sharing your feelings with someone.",
            "Engage in activities that bring you joy.",
            "Celebrate your wins, no matter how small."
        ],
        "NEGATIVE": [
            "It’s okay to feel this way. Try taking deep breaths or writing in a journal.",
            "Reach out to someone you trust to talk about your feelings.",
            "Consider practicing mindfulness or meditation."
        ],
        "NEUTRAL": [
            "Consider doing something relaxing, like a short walk or meditation.",
            "Try listening to music or a podcast that you enjoy.",
            "Engage in a hobby to uplift your mood."
        ]
    }
    return random.choice(strategies.get(sentiment, ["No strategies available."]))