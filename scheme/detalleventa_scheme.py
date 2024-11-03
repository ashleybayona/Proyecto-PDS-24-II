from pydantic import BaseModel
from scheme_base.base_detalleventa import *

class DetalleVenta(AddDetalleVenta):
    idDetalleVenta: int | None = None
    precioUnitario: float | None = None
    precio: float | None = None
