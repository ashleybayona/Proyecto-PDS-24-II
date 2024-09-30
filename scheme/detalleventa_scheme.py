from pydantic import BaseModel

class DetalleVenta(BaseModel):
    IdDetalleVenta: int
    IdVenta: int
    IdProducto: int
    Cantidad: int
    PrecioUnitario: float
    Precio: float 