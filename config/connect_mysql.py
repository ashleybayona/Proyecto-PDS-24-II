import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

conexion_pool = mysql.connector.pooling.MySQLConnectionPool(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
    port=DB_PORT,
    use_pure=True,
    pool_name='mypool',
    pool_size=10
)


if conexion_pool.get_connection().is_connected():
    print("Conexión exitosa a la base de datos en Railway.")
else:
    print("Error en la conexión.")
