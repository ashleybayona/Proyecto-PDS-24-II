#LIBREARÍAS
from fastapi import APIRouter, HTTPException
from typing import List

#ARCHIVOS
from config.connect_gcloud_mysql import *
from scheme.ventas_scheme import *

sales_router = APIRouter()

#PARA VER TODAS LAS VENTAS
@sales_router.get("/ventas", tags=['Venta'], response_model=List[Venta]) #funciona
def get_ventas():
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("select * from venta")
            ventas = cursor.fetchall()
        return ventas
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA CREAR VENTA
@sales_router.post("/ventas", tags=['Venta']) #funciona
def create_venta(iduser: int):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor() as cursor:
            print('aka')
            cursor.callproc('crearventa', [iduser]) 
            print('aka2')
            for resultado in cursor.stored_results():
                id_venta = resultado.fetchone()[0] 
            conexion.commit()
        return {"message": "Venta creada exitosamente", "IdVenta": id_venta}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA ACTUALIZAR LOS IMPORTES EN LA TABLA VENTA
@sales_router.put("/venta/{id_venta}/actualizar-importes", tags=['Venta']) #funciona
def update_importes_venta(id_venta: int):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor() as cursor:
            cursor.callproc('actualizarimportesventa', [id_venta])
            conexion.commit()
        return {"message": "Importes de la venta actualizados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()