import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import logging

load_dotenv()
logger = logging.getLogger(__name__)

pg_username = os.getenv("POSTGRES_USERNAME")
pg_password = os.getenv("POSTGRES_PASSWORD")
pg_db_name = os.getenv("POSTGRES_DB_NAME")
pg_host = os.getenv("POSTGRES_HOST")
pg_port = os.getenv("POSTGRES_PORT")

engine = create_engine(
    f"postgresql+psycopg://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_db_name}"
)

def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except OperationalError as e:
        logger.error("Database connection failed: %s", e)
        return False


if __name__ == "__main__":
    if not test_connection():
        exit(1)