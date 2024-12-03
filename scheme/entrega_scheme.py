from pydantic import BaseModel, validator
from datetime import datetime, timedelta

#ARCHIVOS
from scheme_base.base_entrega import *

class Entrega(BaseModel):
    idEntrega: int
    idFacturacion: int
    #idRepartidor: int
    #fechaEntrega: datetime
    estadoEntrega: EstadoEntrega
    horaEstimada: str
    nombreRepartidor: str
    telefRepartidor: str

    @validator("horaEstimada", pre=True)
    def convertir_timedelta(cls, value):
        if isinstance(value, timedelta):
            # Convierte timedelta a formato HH:MM:SS
            horas, resto = divmod(value.seconds, 3600)
            minutos, segundos = divmod(resto, 60)
            return f"{horas:02}:{minutos:02}:{segundos:02}"
        return value