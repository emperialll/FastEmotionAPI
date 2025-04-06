import requests


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
        "x-rapidapi-key": "a8bee05d6emshdc1205e1fd41c9dp1c50c2jsn387c810cebfb",
        "x-rapidapi-host": "twinword-emotion-analysis-v1.p.rapidapi.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    return response.json()
