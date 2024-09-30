from fastapi import FastAPI, APIRouter, HTTPException
import random, string
from scheme import *
from conexion_sqlserver import * #importa el archivo de la conexión a la bd

app = FastAPI()

app.title = 'API La Puntita' #titulo para la documentación dentro de fastapi

'''
http://127.0.0.1:8000
API para gestionar reservas, aplicando al proyecto: gestionar ventas (aún no las entregas)
- GET: obtener info -> mostrar
- POST: agregar info -> crear
- PUT: reemplazar info -> actualizar
- PATCH: actualizar info
- DELETE: borrar info
'''

@app.get("/", tags=['Home'])
def home():
    return "wasaaaa"


@app.get("/productos", tags=['Producto'], response_model=List[Producto])
def get_productos(): #va a mostrar el diccionario con todos los productos dentro de la bd
    with conexion().cursor() as cursor: #with cierra la conexion autom
        cursor.execute('select * from Producto')
        productos = cursor.fetchall()
    return productos


@app.get("/ventas", tags=['Venta'], response_model=List[Venta])
def get_ventas():
    with conexion().cursor() as cursor:
        cursor.execute("select * from Venta")
        ventas = cursor.fetchall()
        return ventas #cambiar a que de una respuesta http si no encuentra nada!! <- por mejorar

'''
@app.delete("/ventas", tags=['Venta'])#FALTA GAAAA
def delete_venta():
    with conexion().cursor() as cursor:
        cursor.execute
'''

@app.post("/ventas", tags=['Venta'])
def create_venta(iduser: int):
    with conexion().cursor() as cursor:
        try:
            cursor.execute('exec CrearVenta @IdUsuario = ?', (iduser))
            id_venta = cursor.fetchone()[0]

            conexion().commit()
            return {"message": "Venta creada exitosamente", "IdVenta": id_venta}
        
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

@app.post("/detalle-venta", tags=['DetalleVenta'])
def add_detalle_venta(detventa: DetalleVenta):
    with conexion().cursor() as cursor:
        try: 
            cursor.execute('exec AgregarProductosDetalleVenta @IdVenta = ?, @IdProducto = ?, @Cantidad = ?', 
                           (detventa.IdVenta, detventa.IdProducto, detventa.Cantidad))
            conexion().commit()
            return {"message": "Producto agregado a detalle de venta exitosamente"}
        
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

@app.put("/venta/{id_venta}/actualizar-importes", tags=['Venta'])
def update_importes(id_venta: int):
    with conexion().cursor() as cursor:
        try:
            cursor.execute("exec ActualizarImportesVenta @IdVenta = ?", (id_venta))

            conexion().commit()
            return {"message": "Importes de la venta actualizados exitosamente"}
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))