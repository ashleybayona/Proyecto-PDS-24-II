from enum import Enum
import random

class DisponibilidadRepartidor(str, Enum):
    disponible = "disp"
    no_disponible = "no disp"

class RepartidorEliminado(str, Enum):
    eliminado = "elim"
    no_eliminado = "no elim"

def asginarRepartidor(cursor):
    #guardar los repartidores disponibles en una lista
    cursor.execute("select idRepartidor from repartidor where disponibilidad = 'disp' and eliminado = 'no elim'")
    print("despues de ejecutar")
    repartidores = cursor.fetchall()
    print(repartidores)

    #elegir un repartidor aleatorio y retornarlo
    if repartidores:
        idRepartidor = random.choice(repartidores)
        #cambia la disponibilidad del repartidor a no disponible
        cursor.callproc('repartidor_no_disp', [idRepartidor])
        return idRepartidor
    else:
        print("nai repartidores disponibles")
        raise ValueError("No hay repartidores disponibles.")

