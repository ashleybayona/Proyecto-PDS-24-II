from pydantic import BaseModel
from typing import Optional

class Producto(BaseModel):
    IdProducto: int
    IdTipoProducto: int
    NombreProducto: str
    Descripcion: Optional[str]
    PrecioUnitario: float