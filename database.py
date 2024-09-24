# database.py
import pyodbc

def get_db_connection():
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=your_server_name;'
            'DATABASE=your_database_name;'
            'UID=your_username;'
            'PWD=your_password'
        )
        return connection
    except pyodbc.Error as e:
        print("Error al conectar con la base de datos:", e)
        return None
