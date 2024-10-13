import psycopg2

# db connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="tododb",
        user="flaskuser",
        password="123456"
    )
    return conn