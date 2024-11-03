#LIBRERÍAS
from fastapi import APIRouter, HTTPException

#ARCHIVOS
from config.connect_mysql import *
from scheme.detalleventa_scheme import *

sale_detail_router = APIRouter()

#PARA AGREGAR PRODUCTOS AL DETALLE VENTA
@sale_detail_router.post("/detalle-venta", tags=['DetalleVenta']) #funciona
def add_detalle_venta(detventa: AddDetalleVenta):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor() as cursor:
            cursor.callproc('agregarproductodetalleventa', [detventa.idVenta, detventa.idProducto, detventa.cantidad])
            conexion.commit()
        return {"message": "Producto agregado a detalle de venta exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()