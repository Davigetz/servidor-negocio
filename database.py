import psycopg2
from config import Config

def get_db_connection():
    conn = psycopg2.connect(Config.DATABSE_URI)
    return conn
