#LIBRERÍAS
from fastapi import APIRouter, HTTPException
from werkzeug.security import generate_password_hash
from typing import List
import asyncio 

#ARCHIVOS
from config.connect_mysql import *
from scheme.usuario_scheme import *

users_router = APIRouter()

#PARA VER TODOS LOS USUARIOS
@users_router.get("/usuarios", tags=['Usuario'],response_model=List[Usuario]) #funciona
def get_usuarios():
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("select * from usuario")
            usuarios = cursor.fetchall()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA CREAR USUARIO
@users_router.post("/usuario", tags=['Usuario']) #funciona
def create_usuario(data: CreateUser):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor() as cursor:
            new_user = data.dict()
            valid_email = asyncio.run(validar_email(new_user['email']))
            if valid_email:
                new_user["passw"] = generate_password_hash(data.passw, 'pbkdf2:sha256:30', 30)
                cursor.callproc('crear_usuario', [new_user['dni'], new_user['nombre'], new_user['apellido'], new_user['telefono'], 
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
@users_router.put("/user/{id_user}", tags=['Usuario'], response_model=Usuario) #funciona
def update_user(data_update: UpdateUser, id_user: int):
    try:
        conexion = conexion_pool.get_connection()

        with conexion.cursor(dictionary=True) as cursor:
            if data_update.passw:
                passw = generate_password_hash(data_update.passw, 'pbkdf2:sha256:30', 30)
            else:
                passw = data_update.passw
            
            cursor.callproc('update_usuario', [id_user, data_update.telefono, data_update.email, data_update.direccion, data_update.referencia, passw])
            conexion.commit()
            cursor.execute('select * from usuario where idUsuario = %s', (id_user,)) #ya funciona ji
            result = cursor.fetchone()
            
            if result:
                return {
                    "status": "success",
                    "message": "Usuario actualizado correctamente"
                    }
            else:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#PARA ELIMINAR USUARIO
@users_router.delete("/user/{id_user}", tags=['Usuario']) #funciona
def delete_user(id_user: int):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor() as cursor:
            cursor.callproc('delete_usuario', [id_user])
            conexion.commit()
        return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()