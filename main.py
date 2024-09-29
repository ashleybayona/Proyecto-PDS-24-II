from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pyodbc
from conexion_sqlserver import * #importa el archivo de la conexión a la bd

app = FastAPI()

app.title = 'API La Puntita' #titulo para la documentación dentro de fastapi

#http://127.0.0.1:8000

class Producto(BaseModel):
    IdProducto: int
    IdTipoProducto: int
    NombreProducto: str
    Descripcion: str
    PrecioUnitario: float

@app.get("/", tags=['Home'])
def home():
    return "wasaaaa"

@app.get("/productos/", tags=['Producto'])
def get_productos(): #va a mostrar el diccionario con todos los productos dentro de la bd
    conect = conexion()
    cursor = conect.cursor()
    cursor.execute('select IdProducto, IdTipoProducto, NombreProducto, Descripcion, PrecioUnitario from Producto')
    productos = cursor.fetchall()
    conect.close()
    return [{'IdProducto': prod.IdProducto, 'IdTipoProducto': prod.IdTipoProducto,
             'Nombre': prod.NombreProducto, 'Descripción': prod.Descripcion if prod.Descripcion else '-',
             'Precio unitario': prod.PrecioUnitario} for prod in productos] #valores tienen que ser igual al nombre de la columna en la bd al parecer
#    return productos # no sé pq no da con este <- AVERIGUAR

