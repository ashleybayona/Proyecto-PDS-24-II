#LIBRERIAS
from fastapi import APIRouter, HTTPException
from typing import List

#ARCHIVOS
from config.connect_mysql import *
from scheme.productos_scheme import *

products_router = APIRouter()

#PARA VER TODOS LOS PRODUCTOS
@products_router.get("/productos", tags=['Producto'], response_model=List[Producto]) #funciona
def get_productos():
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute('select * from producto')
            productos = cursor.fetchall() 
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#AGREGAR PRODUCTO
#EDITAR PRODUCTO
#ELIMINAR PRODUCTO