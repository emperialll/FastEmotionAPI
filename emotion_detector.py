"""Imports"""
import os
import requests
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()


# Function to connect with Twinword Emotion Analysis
def detect_emotion(user_message):
    """
    Sends a user's message to the Twinword Emotion Analysis API and returns detected emotions.
    Args: user_message (str): The user's message to analyze.
    Returns: dict: A JSON response from the API containing detected emotions and metadata.

    Example response:
        {
            "result_code": "200",
            "emotions_detected": ["joy"],
            ...
        }
    """
    url = "https://twinword-emotion-analysis-v1.p.rapidapi.com/analyze/"

    payload = {"text": user_message}
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("RAPIDAPI_HOST"),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    return response.json()
