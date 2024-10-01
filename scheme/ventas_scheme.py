from pydantic import BaseModel
from datetime import datetime
from .detalleventa_scheme import *

class Venta(BaseModel):
    IdVenta: int | None = None
    IdUsuario: int
    ImporteVenta: float | None = 0
    ImporteIGV: float | None = 0
    ImporteTotal: float | None = 0 
    Fecha: datetime | None = None
    CodigoBoleta: str | None = None
    Estado: int | None = 0