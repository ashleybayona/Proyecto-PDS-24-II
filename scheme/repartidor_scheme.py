from pydantic import BaseModel

#ARCHIVOS
from scheme_base.base_repartidor import *

class Repartidor(BaseModel):
    idRepator: int
    nombre: str
    apellido: str
    telefono: str
    disponibilidad: DisponibilidadRepartidor
    eliminado: RepartidorEliminado