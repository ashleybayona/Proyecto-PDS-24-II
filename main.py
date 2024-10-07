from config.connect_mysql import *
from fastapi import FastAPI, HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from scheme import *
from typing import List

app = FastAPI()

app.title = 'API La Puntita' #titulo para la documentación dentro de fastapi

'''
http://127.0.0.1:8000
API para gestionar reservas, aplicando al proyecto: gestionar ventas (aún no las entregas) -> agregar, editar y eliminar
- GET: obtener info -> mostrar
- POST: agregar info -> crear
- PUT: reemplazar info -> actualizar
- PATCH: actualizar info
- DELETE: borrar info
'''

@app.get("/", tags=['Home'])
def home():
    return "wasaaaa"

@app.get("/productos", tags=['Producto'], response_model=List[Producto]) #funciona
def get_productos():
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute('select * from producto')
            productos = cursor.fetchall() 
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/usuarios", tags=['Usuario'],response_model=List[Usuario]) #funciona
def get_usuarios():
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("select * from usuario")
            usuarios = cursor.fetchall()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/ventas", tags=['Venta'], response_model=List[Venta]) #funciona
def get_ventas():
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("select * from venta")
            ventas = cursor.fetchall()
        return ventas
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/usuario", tags=['Usuario']) #funciona
def create_usuario(data: Usuario):
    try:
        with conexion.cursor() as cursor:
            new_user = data.dict()
            new_user["passw"] = generate_password_hash(data.passw, 'pbkdf2:sha256:30', 30)
            print(data)
            print(new_user)
            cursor.callproc('crearusuario', [new_user['dni'], new_user['nombre'], new_user['apellido'], new_user['telefono'], 
                                            new_user['email'], new_user['direccion'], new_user['referencia'], new_user['passw']])
            conexion.commit()
        return {"message": "Usuario creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/user/{id_user}", tags=['Usuario'], response_model=UpdateUser) #funciona
def update_user(data_update: UpdateUser, id_user: int):
    try:
        with conexion.cursor(dictionary=True) as cursor:
            if data_update.passw:
                passw = generate_password_hash(data_update.passw, 'pbkdf2:sha256:30', 30)
            else:
                passw = data_update.passw
            cursor.callproc('updateusuario', [id_user, data_update.nombre, data_update.apellido, data_update.telefono,
                                            data_update.email, data_update.direccion, data_update.referencia, passw])
            conexion.commit()
            cursor.execute('select * from usuario where idUsuario = %s', (id_user,)) #ya funciona ji
            result = cursor.fetchone()
            return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/user/{id_user}", tags=['Usuario']) #funciona
def delete_user(id_user: int):
    try:
        with conexion.cursor() as cursor:
            cursor.callproc('eliminarusuario', [id_user])
            conexion.commit()
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ventas", tags=['Venta']) #funciona
def create_venta(iduser: int):
    try:
        with conexion.cursor() as cursor:
            print('aka')
            cursor.callproc('crearventa', [iduser]) 
            print('aka2')
            for resultado in cursor.stored_results():
                id_venta = resultado.fetchone()[0] 
            conexion.commit()
        return {"message": "Venta creada exitosamente", "IdVenta": id_venta}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/detalle-venta", tags=['DetalleVenta']) #funciona
def add_detalle_venta(detventa: DetalleVenta):
    try:
        with conexion.cursor() as cursor:
            cursor.callproc('agregarproductodetalleventa', [detventa.idVenta, detventa.idProducto, detventa.cantidad])
            conexion.commit()
        return {"message": "Producto agregado a detalle de venta exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/venta/{id_venta}/actualizar-importes", tags=['Venta']) #funciona
def update_importes_venta(id_venta: int):
    try:
        with conexion.cursor() as cursor:
            cursor.callproc('actualizarimportesventa', [id_venta])
            conexion.commit()
        return {"message": "Importes de la venta actualizados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))