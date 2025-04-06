"""Imports"""
from typing import Union
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from emotion_detector import detect_emotion


app = FastAPI()


class UserInput(BaseModel):
    message: str


REPLIES = {
    "joy": "That's awesome! Pure happiness!",
    "surprise": "Whoa! Didn't expect that!",
    "anger": "That's seriously frustrating!",
    "fear": "Yikes... that's a bit scary.",
    "sadness": "I'm sorry you're feeling that way.",
    "disgust": "Ugh, that's just gross.",
}


def generate_reply(emotion: str) -> str:
    """
    Generates a response based on the detected emotion.
    Args: emotion (str): The emotion detected from the user's message.
    Returns: str: A predefined response corresponding to the emotion.
    """
    return REPLIES.get(
        emotion,
        "Hmm... I can't quite read the vibe. "
        "Want to try saying it another way?"
    )


@app.get("/")
def read_root():
    """
    Root endpoint for testing the API.
    Returns: dict: A welcome message for the Fast Emotion API.
    """
    return {"message": "Welcome to Fast Emotion API"}


@app.post("/conversation")
async def checkEmotion(user_input: UserInput) -> Union[str, dict]:
    """
    Endpoint to analyze user input and return a response based on detected emotion.
    Args: user_input (UserInput): The input message from the user.
    Returns: Union[str, dict]: A string reply based on the emotion detected, 
             or a dict containing an error message.
    """
    try:
        user_emotion = detect_emotion(user_input.message)
        if user_emotion.get("result_code") == "200":
            emotions = user_emotion.get("emotions_detected", [])
            if emotions:
                response_to_user = generate_reply(emotions[0])
                return response_to_user
            else:
                return "Hmm... I can't quite read the vibe. Want to try saying it another way?"
        else:
            return {"error": "Could not detect emotion."}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
