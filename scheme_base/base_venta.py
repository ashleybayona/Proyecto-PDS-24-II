#LIBRERÍAS
from fastapi import HTTPException

#ARCHIVOS
from config.connect_mysql import *

#FUNCION PARA OBTENER EL TOTAL DE LA VENTA
def get_total(idVenta):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor() as cursor:
            #llamada a proc que bota el total y se guarda en una variable
            cursor.callproc('getventatotal', [idVenta, 0])
            for resultado in cursor.stored_results():
                total = resultado.fetchone()[0]
            return total
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

