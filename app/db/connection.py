import psycopg2
from app.config import Config


# establishing db connection
def get_db_connection():
    conn = psycopg2.connect(Config.DATABASE_URI)
    return conn
