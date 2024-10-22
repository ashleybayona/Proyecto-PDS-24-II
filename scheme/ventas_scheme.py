from pydantic import BaseModel
from datetime import datetime
from .detalleventa_scheme import *

class Venta(BaseModel):
    idVenta: int | None = None
    idUsuario: int
    importeVenta: float | None = 0
    importeIGV: float | None = 0
    importeTotal: float | None = 0 
    fecha: datetime | None = None
    codigoBoleta: str | None = None
    estado: int | None = 0