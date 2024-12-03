from pydantic import BaseModel
from datetime import datetime, time

#ARCHIVOS
from scheme_base.base_entrega import *

class Entrega(BaseModel):
    idEntrega: int
    idFacturacion: int
    #idRepartidor: int
    #fechaEntrega: datetime
    estadoEntrega: EstadoEntrega
    horaEstimada: time
    nombreRepartidor: str
    telefRepartidor: str