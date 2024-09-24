import pyodbc

def get_db_connection():
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=ELESEL;'  # Nombre del servidor
            'DATABASE=Proyecto1;'  # Nombre de la base de datos que creaste
            'Trusted_Connection=yes;'  # Autenticación de Windows
        )
        return connection
    except pyodbc.Error as e:
        print("Error al conectar con la base de datos:", e)
        return None
