from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .detalleventa_scheme import *

class Venta(BaseModel):
    IdVenta: int
    IdUsuario: int
    ImporteVenta: Optional[float]  
    ImporteIGV: Optional[float] 
    ImporteTotal: Optional[float]  
    Fecha: Optional[datetime] 
    CodigoBoleta: Optional[str] 
    Estado: Optional[int]  = 0
    Detalles: List[DetalleVenta]