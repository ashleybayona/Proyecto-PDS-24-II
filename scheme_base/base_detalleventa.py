from pydantic import BaseModel

class AddDetalleVenta(BaseModel):
    idVenta: int
    idProducto: int
    cantidad: int