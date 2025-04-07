# Fast Emotion API

A robust FastAPI-based application that analyzes the emotional tone of user messages using the Twinword Emotion Analysis API, generates tailored replies, and persists interactions in a PostgreSQL database. This project detects emotions like joy, surprise, anger, fear, sadness, and disgust, supports multiple emotions per message, and runs seamlessly in a Dockerized environment.

## Features

- **Emotion Detection**: Uses the Twinword Emotion Analysis API to identify single or multiple emotions in text.
- **Dynamic Responses**: Generates rule-based replies, combining responses for multiple emotions (e.g., "That's awesome! Pure happiness! Whoa! Didn't expect that!" for joy and surprise).
- **Database Storage**: Saves each interaction (message, emotions, response) to a PostgreSQL database.
- **RESTful API**: Built with FastAPI, offering intuitive endpoints and Swagger UI.
- **Docker Support**: Fully containerized with Docker Compose for easy deployment.
- **Environment Variables**: Securely manages API keys and database credentials via a `.env` file.

## Prerequisites

- **Python**: Version 3.8 or higher (for local runs).
- **Docker**: Docker and Docker Compose (for containerized runs).
- **API Key**: A valid RapidAPI key for the Twinword Emotion Analysis API (sign up at [RapidAPI](https://rapidapi.com/twinword/api/emotion-analysis-v1)).
- **PostgreSQL**: Required for local runs (e.g., version 16).

## Initial Setup

These steps are required whether you plan to run the app locally or with Docker.

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/emperialll/FastEmotionAPI.git
   cd FastEmotionAPI
   ```

2. **Create and Configure the `.env` File**:
   - Copy the example file:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` in a text editor and fill in your credentials:
     ```
     RAPIDAPI_KEY=your_api_key_here           # Your RapidAPI key from RapidAPI
     RAPIDAPI_HOST=twinword-emotion-analysis-v1.p.rapidapi.com
     DB_PASSWORD=your_postgres_password_here  # Password for PostgreSQL (used locally and in Docker)
     ```
   - **Note on `DB_HOST`**:
     - The `.env.example` includes `DB_HOST=db`, which is used in Docker to connect to the PostgreSQL container named `db`. For local runs, you don’t need to set `DB_HOST` in `.env`—it defaults to `localhost` in the code. Only add `DB_HOST` to `.env` if you’re running PostgreSQL on a different host locally (e.g., `DB_HOST=192.168.1.100`). For Docker, `DB_HOST=db` is set automatically by `docker-compose.yml`, so it’s not required in `.env` unless overriding the default Docker behavior.

## Running Locally

Follow these steps to run the app on your local machine with a local PostgreSQL instance.

1. **Set Up a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up PostgreSQL**:

   - Install PostgreSQL locally (e.g., version 16) if not already installed:
     - Windows: Download from [postgresql.org](https://www.postgresql.org/download/windows/).
     - Mac: `brew install postgresql@16`.
     - Linux: `sudo apt install postgresql postgresql-contrib`.
   - Start PostgreSQL:
     - Mac: `brew services start postgresql@16`.
     - Linux: `sudo systemctl start postgresql`.
   - Create the database:
     ```bash
     psql -U postgres -c "CREATE DATABASE emotion_api_db;"
     ```
   - Ensure your `DB_PASSWORD` in `.env` matches your local PostgreSQL `postgres` user password.

4. **Start the Application**:

   ```bash
   python main.py
   ```

   - The API will be available at `http://127.0.0.1:8000`.
   - Access Swagger UI at `http://127.0.0.1:8000/docs`.

5. **Check Saved Data in the Database**:
   - After sending requests to `/conversation`, verify the stored interactions:
     ```bash
     psql -U postgres -d emotion_api_db
     ```
   - Run:
     ```sql
     SELECT * FROM interactions;
     ```
   - Example output:
     ```
      id | message              | emotion | response                     | timestamp
     ----+----------------------+---------+------------------------------+-------------------------
      1  | I just won the lottery! | joy     | That's awesome! Pure happiness! | 2025-04-07 ...
     ```
   - Exit with: `\q`

## Running with Docker

Follow these steps to run the app in a containerized environment using Docker Compose.

1. **Install Docker and Docker Compose**:

   - Download [Docker Desktop](https://www.docker.com/products/docker-desktop) (Windows/Mac) or follow [Linux instructions](https://docs.docker.com/engine/install/).
   - Verify: `docker --version` and `docker-compose --version`.

2. **Build and Run**:

   - Ensure your `.env` file is set up (from Initial Setup) with `RAPIDAPI_KEY`, `RAPIDAPI_HOST`, and `DB_PASSWORD`.
   - Run:
     ```bash
     docker-compose up --build
     ```
   - This builds the FastAPI app container and starts a PostgreSQL container.
   - The API will be available at `http://127.0.0.1:8000`.
   - Test with:
     ```bash
     curl -X POST "http://127.0.0.1:8000/conversation" -H "Content-Type: application/json" -d '{"message": "I feel great!"}'
     ```

3. **Check Saved Data in the Database**:

   - While the app is running, open a new terminal.
   - Find the PostgreSQL container name:
     ```bash
     docker ps
     ```
     - Look for the `postgres:16` image (e.g., `fastemotionapi_db_1`).
   - Access the database:
     ```bash
     docker exec -it <container_name> psql -U postgres -d emotion_api_db
     ```
     - Replace `<container_name>` with the actual name (e.g., `fastemotionapi_db_1`).
   - Run:
     ```sql
     SELECT * FROM interactions;
     ```
   - Example output:
     ```
      id | message              | emotion | response                     | timestamp
     ----+----------------------+---------+------------------------------+-------------------------
      1  | I feel great!        | joy     | That's awesome! Pure happiness! | 2025-04-07 ...
     ```
   - Exit with: `\q`

4. **Stop the Application**:
   - Press `Ctrl+C` in the `docker-compose` terminal.
   - Clean up:
     - Keep data: `docker-compose down`
     - Reset data: `docker-compose down -v`

## API Endpoints

### `GET /`

- **Description**: A root endpoint to test the API.
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

- **Description**: Analyzes a user’s message, detects emotions, saves the interaction to PostgreSQL, and returns emotions with a combined reply.
- **Request Body**: JSON with a `message` field (string).
- **Response**: JSON with detected emotions and reply, or an error message.
- **Examples**:
  - Single emotion:
    ```bash
    curl -X POST "http://127.0.0.1:8000/conversation" \
         -H "Content-Type: application/json" \
         -d '{"message": "I just won the lottery!"}'
    ```
    **Response**:
    ```json
    { "emotions": ["joy"], "response": "That's awesome! Pure happiness!" }
    ```
  - Multiple emotions:
    ```bash
    curl -X POST "http://127.0.0.1:8000/conversation" \
         -H "Content-Type: application/json" \
         -d '{"message": "I was stunned to see a stranger claiming to be me!"}'
    ```
    **Response**:
    ```json
    {
      "emotions": ["surprise", "anger"],
      "response": "Whoa! Didn't expect that! That's seriously frustrating!"
    }
    ```
  - No emotion detected:
    ```json
    {
      "response": "Hmm... I can't quite read the vibe. Want to try saying it another way?"
    }
    ```
  - Error:
    ```json
    { "error": "Could not detect emotion." }
    ```

## How It Works

1. **Input**: User sends a message via `/conversation`.
2. **Emotion Detection**: `emotion_detector.py` queries the Twinword API.
3. **Response Generation**: `main.py` combines predefined replies for all detected emotions.
4. **Storage**: `db_manager.py` saves the message, emotions (as a string), and response to PostgreSQL.
5. **Output**: Returns a JSON object with emotions and reply.

## Supported Emotions and Replies

| Emotion  | Reply                                |
| -------- | ------------------------------------ |
| Joy      | "That's awesome! Pure happiness!"    |
| Surprise | "Whoa! Didn't expect that!"          |
| Anger    | "That's seriously frustrating!"      |
| Fear     | "Yikes... that's a bit scary."       |
| Sadness  | "I'm sorry you're feeling that way." |
| Disgust  | "Ugh, that's just gross."            |

Multiple emotions combine replies with spaces (e.g., "joy, surprise" → "That's awesome! Pure happiness! Whoa! Didn't expect that!"). A fallback reply is used if no emotions are detected.

## Project Structure

```
fast-emotion-api/
├── main.py              # FastAPI app and endpoint definitions
├── emotion_detector.py  # Twinword API integration
├── db_manager.py        # PostgreSQL initialization and storage
├── .env                 # Environment variables (not in repo)
├── .env.example         # Template for environment variables
├── requirements.txt     # Project dependencies
├── Dockerfile           # Docker config for the app
├── docker-compose.yml   # Docker Compose config for app + PostgreSQL
└── README.md            # This file
```

## Dependencies

See `requirements.txt`. Key libraries:

- `fastapi`: API framework.
- `uvicorn`: ASGI server.
- `requests`: HTTP requests to Twinword API.
- `psycopg2-binary`: PostgreSQL driver.
- `python-dotenv`: Environment variable management.
- `pydantic`: Request validation.

## Notes

- Requires an active RapidAPI subscription for Twinword API.
- Error handling is basic; consider logging or retries for production.
- Dockerized setup uses a persistent volume for PostgreSQL data.

## Contributing

Submit issues or pull requests on GitHub. Ideas for enhancements (e.g., custom replies, advanced error handling) are welcome.

## License

Unlicensed—free to use, modify, and distribute.
