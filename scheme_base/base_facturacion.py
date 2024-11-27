from pydantic import BaseModel
from datetime import datetime
from fastapi import HTTPException
import json

#ARCHIVOS
from config.connect_mysql import *
from scheme.det_facturacion_scheme import *

class BaseFacturacion(BaseModel):
    idFacturacion: int
    fecha: datetime
    importeVenta: float
    importeDelivery: float
    importeIGV: float
    importeTotal: float
    codigoBoleta: str
    tipoDocumento: str

def calcularImportes(productos, cursor): #devuelve importeVenta, importeIGV / productos: {idProducto, cantidad}
    subtotal = 0.00
    productosCalculados = []

    for producto in productos:
        print(producto) #{'idProducto': 24, 'cantidad': 2}
        cursor.execute("select precioUnitario, nombreProducto from producto where idProducto = %s", [producto["idProducto"],]) 
        result = cursor.fetchone()  #result = {'precioUnitario': Decimal('16.00')}

        if not result: 
            raise ValueError(f"Producto {producto['idProducto']} no encontrado")
        
        #establece los montos de los productos
        producto["nombreProducto"] = result['nombreProducto']
        preciounit =  float(result['precioUnitario'])
        producto["precioUnitario"] = preciounit
        producto["precio"] = preciounit * producto["cantidad"]
        subtotal += producto["precio"]

        productosCalculados.append(producto)
    
    #modificado para que salgan los precios esperados 0.18 * PRECIO + PRECIO = PRECIO TOTAL
    precioTotalProductos = subtotal / 1.18 
    igv = precioTotalProductos * 0.18

    return precioTotalProductos, igv, productosCalculados

#primero crea la fila en factura introduciento los datos y esto regresa el idFacturacion para poder agregar los productos a detalleFactura
def guardarCompra(iduser, session):
    print("entra a guardarCompra")
    metadata = session["metadata"]
    print("metadata", metadata)
    conexion = None
    try:
        print("entra al try")
        # ver si están todos los datos
        required_keys = ["impVenta", "impDelivery", "impIGV", "impTotal", "productos", "tipoDocumento"]
        for key in required_keys:
            if key not in metadata:
                raise ValueError(f"Falta el campo requerido en metadata: {key}")
        
        print("despues de los required_keys")

        # volver al tipo de dato original
        impVenta = round(float(metadata["impVenta"]), 2)
        print(impVenta)
        impDelivery = round(float(metadata["impDelivery"]), 2)
        print(impDelivery)
        impIGV = round(float(metadata["impIGV"])), 2        
        print(impIGV)
        impTotal = round(float(metadata["impTotal"]), 2)
        print(impTotal)
        productos = json.loads(metadata["productos"])
        print(productos)

        print("antes de conexion")

        conexion = conexion_pool.get_connection()

        with conexion.cursor() as cursor:
            print("entre al cursor")

            #crea fila en factura
            cursor.callproc('insertar_facturacion', [iduser, impVenta, impDelivery, impIGV, impTotal, metadata["tipoDocumento"], session["id"]])

            print("despues de insertar_facturacion")
            print(session["id"])

            # obtener el id para el detalle de factura
            for result in cursor.stored_results():
                idFacturacion = result.fetchone()[0]

            if not idFacturacion:
                raise ValueError("No se pudo obtener el ID de la facturación.")

            print("va a entrar a guardarProducto")
            #agrega productos a detalleFactura con el idFacturacion obtenido
            guardarProducto(idFacturacion, productos, cursor)

            print("sale de guardarProducto")

            conexion.commit()
            return {
                "status": "success", 
                "idFacturacion": idFacturacion
                }
    except ValueError as e:
        # Error específico de validación o lógica
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al guardar la compra: {str(e)}")
    finally:
        if conexion and conexion.is_connected():
            conexion.close()