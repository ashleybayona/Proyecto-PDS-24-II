from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from werkzeug.security import generate_password_hash, check_password_hash
from config.connect_gcloud_mysql import *
from scheme import *
from typing import List
import uvicorn
import asyncio 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)

app.title = 'API La Puntita' 

@app.get("/", tags=['Home'])
def home():
    return "wasaaaa"

#PARA VER TODOS LOS PRODUCTOS
@app.get("/productos", tags=['Producto'], response_model=List[Producto]) #funciona
def get_productos():
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute('select * from producto')
            productos = cursor.fetchall() 
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA VER TODOS LOS USUARIOS
@app.get("/usuarios", tags=['Usuario'],response_model=List[Usuario]) #funciona
def get_usuarios():
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("select * from usuario")
            usuarios = cursor.fetchall()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA VER TODAS LAS VENTAS
@app.get("/ventas", tags=['Venta'], response_model=List[Venta]) #funciona
def get_ventas():
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("select * from venta")
            ventas = cursor.fetchall()
        return ventas
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA CREAR USUARIO
@app.post("/usuario", tags=['Usuario']) #funciona
def create_usuario(data: CreateUser):
    try:
        with conexion.cursor() as cursor:
            new_user = data.dict()
            valid_email = asyncio.run(validar_email(new_user['email']))#new_user['email']
            if valid_email:
                new_user["passw"] = generate_password_hash(data.passw, 'pbkdf2:sha256:30', 30)
                cursor.callproc('crearusuario', [new_user['dni'], new_user['nombre'], new_user['apellido'], new_user['telefono'], 
                                                new_user['email'], new_user['direccion'], new_user['referencia'], new_user['passw']])
            else:
                raise HTTPException(status_code=400, detail="El correo electrónico no es válido.")
            conexion.commit()
        return {"message": "Usuario creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA ACTUALIZAR USUARIO
@app.put("/user/{id_user}", tags=['Usuario'], response_model=Usuario) #funciona
def update_user(data_update: UpdateUser, id_user: int):
    try:
        with conexion.cursor(dictionary=True) as cursor:
            if data_update.passw:
                passw = generate_password_hash(data_update.passw, 'pbkdf2:sha256:30', 30)
            else:
                passw = data_update.passw
            cursor.callproc('updateusuario', [id_user, data_update.telefono, data_update.email, data_update.direccion, data_update.referencia, passw])
            conexion.commit()
            cursor.execute('select * from usuario where idUsuario = %s', (id_user,)) #ya funciona ji
            result = cursor.fetchone()
            return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA ELIMINAR USUARIO
@app.delete("/user/{id_user}", tags=['Usuario']) #funciona
def delete_user(id_user: int):
    try:
        with conexion.cursor() as cursor:
            cursor.callproc('eliminarusuario', [id_user])
            conexion.commit()
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA CREAR VENTA
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
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA AGREGAR PRODUCTOS AL DETALLE VENTA
@app.post("/detalle-venta", tags=['DetalleVenta']) #funciona
def add_detalle_venta(detventa: DetalleVenta):
    try:
        with conexion.cursor() as cursor:
            cursor.callproc('agregarproductodetalleventa', [detventa.idVenta, detventa.idProducto, detventa.cantidad])
            conexion.commit()
        return {"message": "Producto agregado a detalle de venta exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA ACTUALIZAR LOS IMPORTES EN LA TABLA VENTA
@app.put("/venta/{id_venta}/actualizar-importes", tags=['Venta']) #funciona
def update_importes_venta(id_venta: int):
    try:
        with conexion.cursor() as cursor:
            cursor.callproc('actualizarimportesventa', [id_venta])
            conexion.commit()
        return {"message": "Importes de la venta actualizados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)