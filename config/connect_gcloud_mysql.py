import mysql.connector
import os

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

conexion = mysql.connector.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
    use_pure=True
)


if conexion.is_connected():
    print("Conexión exitosa a la base de datos en Google Cloud SQL.")
else:
    print("Error en la conexión.")