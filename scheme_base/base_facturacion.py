from pydantic import BaseModel
from datetime import datetime

class BaseFacturacion(BaseModel):
    idFacturacion: int
    fecha: datetime
    importeVenta: float
    importeDelivery: float
    importeIGV: float
    importeTotal: float
    codigoBoleta: str
    tipoDocumento: str

