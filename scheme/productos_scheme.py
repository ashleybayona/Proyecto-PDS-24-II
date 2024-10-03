from pydantic import BaseModel

class Producto(BaseModel):
    idProducto: int | None = None
    idTipoProducto: int
    nombreProducto: str
    descripcion: str | None = None
    precioUnitario: float