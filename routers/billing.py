#LIBREARÍAS
from fastapi import APIRouter, HTTPException
from typing import List

#ARCHIVOS
from config.connect_mysql import *
from scheme.facturacion_scheme import *

billing_router = APIRouter()

#PARA VER TODAS LAS VENTAS
@billing_router.get("/facturaciones", tags=['Facturacion'], response_model=List[Facturacion]) #funciona
def get_ventas():
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("select * from facturacion")
            ventas = cursor.fetchall()
        return ventas
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA VER VENTAS POR USUARIO
@billing_router.get("/historial", tags=['Facturacion'], response_model=List[Compra]) #funciona
def get_historial_compras(iduser: int):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            cursor.callproc('compras_usuario', [iduser])
            
            for result in cursor.stored_results():
                compras = result.fetchall()

            if not compras:
                raise HTTPException(status_code=404, detail="No se encontraron compras para este usuario")
            
            # Organizar las compras
            historial = {}
            for compra in compras:
                id_fact = compra['idFacturacion']

                if id_fact not in historial:
                    historial[id_fact] = {
                        "idFacturacion": id_fact,
                        "fecha": compra['fecha'],
                        "codigoBoleta": compra['codigoBoleta'],
                        "tipoDocumento": compra['tipoDocumento'],
                        "importeVenta": compra['importeVenta'],
                        "importeDelivery": float(compra['importeDelivery']),
                        "importeIGV": float(compra['importeIGV']),
                        "importeTotal": float(compra['importeTotal']),
                        "detalles": []
                    }
                
                historial[id_fact]["detalles"].append({
                    "nombreProducto": compra['nombreProducto'],
                    "precioUnitVenta": float(compra['precioUnitVenta']),
                    "cantidad": compra['cantidad'],
                    "precio": float(compra['precio'])
                })
            
            return list(historial.values())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

'''#YA NO SIRVE CREO PARA CREAR FACTURACION: SIGNIFICA QUE YA HA SIDO PAGADA
@billing_router.post("/ventas", tags=['Venta']) #EDITAR
def create_venta(iduser: int):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor() as cursor:
            print('aka')
            cursor.callproc('crearventa', [iduser, 0]) 
            print('aka2')
            for resultado in cursor.stored_results():
                id_venta = resultado.fetchone()[0] 
            conexion.commit()
        return {"message": "Venta creada exitosamente", "IdVenta": id_venta}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()'''


'''#YA NO SIRVE CREO PARA ACTUALIZAR LOS IMPORTES EN LA TABLA VENTA
@billing_router.put("/venta/{id_venta}/actualizar-importes", tags=['Venta']) #funciona
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
            conexion.close()'''

