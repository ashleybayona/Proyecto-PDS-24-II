from fastapi import HTTPException
from pydantic import BaseModel

def guardarProducto(idFacturacion, productos, cursor):
    print("entra a guardarProducto")
    try:
        print("entra al try")

        for producto in productos:
            cursor.callproc('add_prod_det_fact', [idFacturacion, producto["idProducto"], producto["cantidad"]])

        print("paso el for")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error agregando productos a la factura: {str(e)}")