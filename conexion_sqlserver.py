import pyodbc

def conexion():
    try:
        connection = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=LAPTOPASHLEY; DATABASE=LaPuntita;Trusted_Connection=yes')
        print("Conexión exitosa")
        return connection
    except Exception as ex:
        print(ex)
#    finally:
#        connection.close()
#        print("Conexión finalizada")