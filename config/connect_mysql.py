import mysql.connector

conexion = mysql.connector.connect(
    user = 'root',
    password = '25MysQl17',
    host = 'localhost',
    database = 'lapuntita',
    port = '3306'
)

print(conexion)