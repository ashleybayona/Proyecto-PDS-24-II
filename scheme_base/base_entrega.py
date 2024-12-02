from enum import Enum
from fastapi import HTTPException

#ARCHIVOS
from scheme.repartidor_scheme import *

class EstadoEntrega(str, Enum):
    pendiente = "pendiente"
    en_proceso = "en proceso"
    entregado = "entregado"

#FUNCION PARA AGREGAR ENTREGA
def crearEntrega(idFacturacion, cursor):
    try:
        #obtener el idRepartidor
        idRepartidor = asginarRepartidor(cursor)
        print(idRepartidor)

        #crear la entrega
        cursor.callproc('agregar_entrega', [idFacturacion, idRepartidor]) #pone a la entrega en proceso

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear la entrega: {str(e)}")
