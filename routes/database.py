from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT
import mysql.connector

def get_db_connection():
    print("Connecting with user:", MYSQL_USER)
    print("Password used:", MYSQL_PASSWORD)  # Don't do this in production!

    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT
    )
