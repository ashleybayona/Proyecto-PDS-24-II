from pydantic import BaseModel

#ARCHIVOS
from scheme_base.base_det_facturacion import *

class DetalleFacturacion(BaseModel):
    idDetFacturacion: int 
    idFacturacion: int
    idProducto: int
    precioUnitario: float 
    precioUnitVenta: float
    cantidad: int
    precio: float 

class DetalleCompra(BaseModel):
    nombreProducto: str 
    precioUnitVenta: float
    cantidad: int
    precio: float
