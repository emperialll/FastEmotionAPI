import requests


def detect_emotion(user_message):
    url = "https://twinword-emotion-analysis-v1.p.rapidapi.com/analyze/"

    payload = {"text": user_message}
    headers = {
        "x-rapidapi-key": "a8bee05d6emshdc1205e1fd41c9dp1c50c2jsn387c810cebfb",
        "x-rapidapi-host": "twinword-emotion-analysis-v1.p.rapidapi.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    return response.json()
