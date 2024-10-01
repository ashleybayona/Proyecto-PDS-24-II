from pydantic import BaseModel

class Producto(BaseModel):
    IdProducto: int | None = None
    IdTipoProducto: int
    NombreProducto: str
    Descripcion: str | None = None
    PrecioUnitario: float