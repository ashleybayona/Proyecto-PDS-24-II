from pydantic import BaseModel

class DetalleVenta(BaseModel):
    idDetalleVenta: int | None = None
    idVenta: int
    idProducto: int
    cantidad: int
    precioUnitario: float | None = None
    precio: float | None = None