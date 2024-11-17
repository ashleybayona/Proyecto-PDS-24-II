#LIBRERÍAS
from fastapi import APIRouter, HTTPException

#ARCHIVOS
from config.connect_mysql import *
from scheme.det_facturacion_scheme import *

billing_detail_router = APIRouter()

'''#YA NO SIRVE CREO PARA AGREGAR PRODUCTOS AL DETALLE VENTA
@billing_detail_router.post("/detalle-venta", tags=['DetalleVenta']) #EDITAR 
def add_detalle_venta(detventa: AddDetalleFacturacion):
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
            conexion.close()'''