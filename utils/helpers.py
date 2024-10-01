# utils/helpers.py
from transformers import pipeline

def analyze_sentiment(text):
    sentiment_analyzer = pipeline("sentiment-analysis")
    result = sentiment_analyzer(text)
    return {
        "label": result[0]['label'],
        "score": result[0]['score']
    }
