from pydantic import BaseModel

class DetalleVenta(BaseModel):
    IdDetalleVenta: int | None = None
    IdVenta: int
    IdProducto: int
    Cantidad: int
    PrecioUnitario: float | None = None
    Precio: float | None = None