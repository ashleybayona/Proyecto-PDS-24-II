#LIBRERÍAS
from fastapi import APIRouter, HTTPException

#ARCHIVOS
from config.connect_mysql import *
from scheme.entrega_scheme import *

entrega_router = APIRouter()

#ver el estado de la entrega solo si sigue como "en proceso", para el seguimiento del pedido
