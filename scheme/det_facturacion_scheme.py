from pydantic import BaseModel

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
