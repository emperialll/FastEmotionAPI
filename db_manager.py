"""Database management module for PostgreSQL interactions."""
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global connection variable
_conn = None


def get_db_connection():
    """
    Returns a connection to the PostgreSQL database, creating it if it doesn't exist.
    Uses environment variables for connection details.
    Returns: psycopg2.connection: A connection object to the database.
    """
    global _conn
    if _conn is None or _conn.closed:
        try:
            _conn = psycopg2.connect(
                dbname="emotion_api_db",
                user="postgres",
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST", "localhost"),
                port="5432"
            )
            print("Database connection established.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise
    return _conn


def init_db():
    """
    Initializes the PostgreSQL database by creating the interactions table if it doesn't exist.
    Uses environment variables for connection details.
    """
    conn = None
    cur = None
    try:
        # Connect to the database
        conn = get_db_connection()
        # Create a cursor
        cur = conn.cursor()
        # Create the interactions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                emotion VARCHAR(50),
                response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Commit the changes
        conn.commit()
        print("Interactions table created successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        # Close cursor and connection only if they exist
        if cur is not None:
            cur.close()


def save_interaction(message: str, emotions: list, response: str):
    """
    Saves an interaction to the interactions table.
    Args:
        message (str): The user's input message.
        emotions (list): The list of detected emotions.
        response (str): The generated response.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Join emotions list into a single string
        emotions_str = ", ".join(emotions)
        cur.execute(
            "INSERT INTO interactions (message, emotion, response) VALUES (%s, %s, %s)",
            (message, emotions_str, response)
        )
        conn.commit()
        print("Interaction saved successfully.")
    except Exception as e:
        print(f"Error saving interaction: {e}")
        conn.rollback()
    finally:
        if cur:
            cur.close()
