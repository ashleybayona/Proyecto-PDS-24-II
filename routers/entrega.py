#LIBRERÍAS
from fastapi import APIRouter, HTTPException

#ARCHIVOS
from config.connect_mysql import *
from scheme.entrega_scheme import *

entrega_router = APIRouter()

#ver el estado de la entrega solo si sigue como "en proceso", para el seguimiento del pedido ESTO ES DENTRO DEL PERFIL USUARIO EN EL APARTADO SEGUIMIENTO DE PEDIDO
@entrega_router.get("/mi-cuenta/seguimiento-pedidos", tags=["Usuario"], response_model=Entrega) 
def seguimiento_pedidos(id: int):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            cursor.callproc('seguimiento_pedido_usuario', [id])
            for result in cursor.stored_results():
                pedidos = result.fetchall() # guarda todos los que pedidos que no estan como entregados
        return {"status": "success", "pedidos": pedidos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los pedidos: {str(e)}")
    finally:
        if conexion and conexion.is_connected():
            conexion.close()

#otro endpoint que se muestra despues de haber hecho la compra donde se muestra la informacion del pedido recién pagado
@entrega_router.get("/checkout/entrega", tags=["Entrega"], response_model=Entrega)
def info_entrega(id: int):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            cursor.callproc('info_entrega', [id])

            for result in cursor.stored_results():
                info_entrega = result.fetchone()
            
            if not info_entrega:
                raise HTTPException(status_code=404, detail="No se encontró información para la entrega.")

        return {"status": "success", "entrega": info_entrega}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la entrega: {str(e)}")
    finally:
        if conexion and conexion.is_connected():
            conexion.close()
