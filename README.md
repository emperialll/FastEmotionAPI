# Fast Emotion API

A simple FastAPI-based application that analyzes the emotional tone of user messages using the Twinword Emotion Analysis API and responds with a tailored reply. This project detects emotions like joy, surprise, anger, fear, sadness, and disgust, and generates human-like responses based on the dominant emotion.

## Features

- **Emotion Detection**: Leverages the Twinword Emotion Analysis API to identify emotions in text.
- **Dynamic Responses**: Returns predefined, emotion-specific replies (e.g., "That's awesome!" for joy).
- **RESTful API**: Built with FastAPI, offering easy-to-use endpoints.
- **Environment Variables**: Securely manages API keys using a `.env` file.

## Prerequisites

- **Python**: Version 3.8 or higher.
- **API Key**: A valid RapidAPI key for the Twinword Emotion Analysis API (sign up at [RapidAPI](https://rapidapi.com/twinword/api/emotion-analysis-v1)).

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/emperialll/FastEmotionAPI.git
   ```

2. **Set Up a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and replace `your_api_key_here` with your RapidAPI key:
     ```
     RAPIDAPI_KEY=your_api_key_here
     RAPIDAPI_HOST=twinword-emotion-analysis-v1.p.rapidapi.com
     ```

## Running the Application

Start the FastAPI server:

```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive Swagger UI at `http://127.0.0.1:8000/docs` for testing endpoints.

## API Endpoints

### `GET /`

- **Description**: A simple root endpoint to test the API.
- **Response**: JSON welcome message.
- **Example**:
  ```bash
  curl http://127.0.0.1:8000/
  ```
  **Response**:
  ```json
  { "message": "Welcome to Fast Emotion API" }
  ```

### `POST /conversation`

- **Description**: Analyzes the emotion in a user’s message and returns a tailored reply.
- **Request Body**: JSON with a `message` field (string).
- **Response**: Either a string reply or a JSON error object.
- **Example**:
  ```bash
  curl -X POST "http://127.0.0.1:8000/conversation" \
       -H "Content-Type: application/json" \
       -d '{"message": "I just won the lottery!"}'
  ```
  **Response**:
  ```
  "That's awesome! Pure happiness!"
  ```
  - If no emotion is detected:
    ```
    "Hmm... I can't quite read the vibe. Want to try saying it another way?"
    ```
  - If an error occurs:
    ```json
    { "error": "Could not detect emotion." }
    ```

## How It Works

1. **Input**: The user sends a message via the `/conversation` endpoint.
2. **Emotion Detection**: The `emotion_detector.py` module queries the Twinword API with the message.
3. **Response Generation**: The app checks the API response, extracts the primary emotion (if any), and selects a reply from a predefined dictionary.
4. **Output**: Returns the reply or an error message if something goes wrong.

## Supported Emotions and Replies

| Emotion  | Reply                                |
| -------- | ------------------------------------ |
| Joy      | "That's awesome! Pure happiness!"    |
| Surprise | "Whoa! Didn't expect that!"          |
| Anger    | "That's seriously frustrating!"      |
| Fear     | "Yikes... that's a bit scary."       |
| Sadness  | "I'm sorry you're feeling that way." |
| Disgust  | "Ugh, that's just gross."            |

If no emotion is detected or an unrecognized emotion is returned, a fallback message is used.

## Project Structure

```
fast-emotion-api/
├── main.py              # FastAPI app and endpoint definitions
├── emotion_detector.py  # Twinword API integration
├── .env.example         # Example environment variable file
├── requirements.txt     # Project dependencies
└── README.md            # This file
```

## Dependencies

Listed in `requirements.txt`. Key libraries include:

- `fastapi`: For building the API.
- `uvicorn`: ASGI server to run the app.
- `requests`: For making HTTP requests to the Twinword API.
- `python-dotenv`: For loading environment variables.
- `pydantic`: For request validation.

## Notes

- The Twinword API requires a valid subscription on RapidAPI. Ensure your key is active and has quota available.
- Error handling is basic in this version; enhance it for production use (e.g., logging, retry logic).
- The app runs locally by default. For deployment, consider a production-grade server like Gunicorn with Uvicorn.

## Contributing

Feel free to submit issues or pull requests! Suggestions for new features (e.g., custom replies, multi-emotion support) are welcome.

## License

This project is unlicensed—free to use, modify, and distribute as you see fit.
