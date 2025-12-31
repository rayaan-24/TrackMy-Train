import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="0061@BCA",
        database="trackmytrain_db"
    )
