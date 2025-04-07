import os
import time
import psycopg2
from psycopg2 import OperationalError


def wait_for_db():
    host = os.getenv("DB_HOST", "localhost")
    dbname = "emotion_api_db"
    user = "postgres"
    password = os.getenv("DB_PASSWORD")
    port = "5432"
    max_attempts = 30
    attempt = 1

    while attempt <= max_attempts:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.close()
            print("Database is ready!")
            return
        except OperationalError as e:
            print(f"Waiting for database... Attempt {attempt}/{max_attempts}")
            time.sleep(1)
            attempt += 1
    raise Exception("Database not ready after maximum attempts.")


if __name__ == "__main__":
    wait_for_db()
