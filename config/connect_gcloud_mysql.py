import mysql.connector

conexion = mysql.connector.connect(
    user='lapuntita',                             # Nombre de usuario
    password='lapuntita123',                    # Contraseña
    host='34.39.134.121',                    # IP pública de la instancia o Cloud SQL Auth Proxy
    database='lapuntita',                    # Nombre de la base de datos
    port='3306',                             # Puerto
    #ssl_ca='server-ca.pem',                  # Ruta al certificado del servidor ../config/
    #ssl_cert='client-cert.pem',              # Ruta al certificado del cliente  config/client-cert.pem
    #ssl_key='client-key.pem'                 # Ruta a la clave privada del cliente
)

if conexion.is_connected():
    print("Conexión exitosa a la base de datos en Google Cloud SQL.")
else:
    print("Error en la conexión.")