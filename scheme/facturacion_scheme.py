from typing import List
from datetime import datetime

#ARCHIVOS
from scheme_base.base_facturacion import *
from scheme.det_facturacion_scheme import *

class Facturacion(BaseFacturacion):
    idUsuario: int
    idStripe: str | None = 0
    estadoPago: str 

class Compra(BaseFacturacion):
    detalles: List[DetalleCompra]

