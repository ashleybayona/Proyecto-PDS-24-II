# database.py
import pyodbc

def get_db_connection():
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=ELESEL;'  # Nombre del servidor
            'DATABASE=Proyecto1;'  # Nombre de la base de datos
            'Trusted_Connection=yes;'  # Autenticación de Windows
        )
        print("Conexión exitosa a la base de datos")  # Mensaje de éxito
        return connection
    except pyodbc.Error as e:
        print("Error al conectar con la base de datos:", e)
        return None

# Prueba la conexión ejecutando una consulta simple
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Consulta sencilla de prueba
        result = cursor.fetchone()
        print("Resultado de la consulta de prueba:", result)
        conn.close()
