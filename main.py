from fastapi import FastAPI, HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from scheme import *
from conexion_sqlserver import * #importa el archivo de la conexión a la bd
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


@app.get("/productos", tags=['Producto'], response_model=List[Producto]) #SÍ FUNCIONA
def get_productos(): #va a mostrar el diccionario con todos los productos dentro de la bd
    with conexion().cursor() as cursor: #with cierra la conexion autom
        cursor.execute('select * from Producto')
        productos = cursor.fetchall()
    return productos

@app.get("/usuarios", tags=['Usuario'], response_model=List[Usuario]) #SÍ FUNCIONA
def get_usuarios():
    try: 
        with conexion().cursor() as cursor:
            cursor.execute("select * from Usuario")
            usuarios = cursor.fetchall()
        return usuarios
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/ventas", tags=['Venta'], response_model=List[Venta]) #SÍ FUNCIONA GAAA
def get_ventas():
    try: 
        with conexion().cursor() as cursor:
            cursor.execute("select * from Venta")
            ventas = cursor.fetchall()
        return ventas #cambiar a que de una respuesta http si no encuentra nada!! <- por mejorar
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

'''
@app.delete("/ventas", tags=['Venta'])#FALTA GAAAA
def delete_venta():
    with conexion().cursor() as cursor:
        cursor.execute
'''

@app.post("/usuario", tags=['Usuario']) #SÍ FUNCIONA
def create_usuario(data: Usuario):
    try:
        with conexion().cursor() as cursor:
            new_user = data.dict()
            #para encriptar la contraseña y que no sea visible en la base de datos 
            new_user["Contrasenia"] = generate_password_hash(data.Contrasenia, 'pbkdf2:sha256:30', 30)
            
            consulta = '''exec CrearUsuario @DNI = ?, @Nombre = ?, @Apellido = ?, @Telefono = ?,
            @Email = ?, @Direccion = ?, @Referencia = ?, @Contrasenia = ?'''
            cursor.execute(consulta, (new_user['DNI'], new_user['Nombre'], new_user['Apellido'], new_user['Telefono'],
                                    new_user['Email'], new_user['Direccion'], new_user['Referencia'], new_user['Contrasenia']))
        return {"message": "Usuario creado exitosamente", "Nombre": new_user['Nombre']}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/user/{id_user}", tags=['Usuario'], response_model=UpdateUser)
def update_user(data_update: UpdateUser, userid: int):
    try:
        with conexion().cursor() as cursor:
            if data_update.Contrasenia:
                passw = generate_password_hash(data_update.Contrasenia, 'pbkdf2:sha256:30', 30)
            else:
                passw = data_update.Contrasenia #que quede null si no se cambia para que en la base de datos quede la anterior

            consulta = '''exec UpdateUser @IdUsuario = ?, @Nombre = ?, @Apellido = ?, @Telefono = ?,
            @Email = ?, @Direccion = ?, @Referencia = ?, @Contrasenia = ?'''
            cursor.execute(consulta, (userid, data_update.Nombre, data_update.Apellido, data_update.Telefono,
                                      data_update.Email, data_update.Direccion, data_update.Referencia, passw))
            conexion().commit()
            result = cursor.execute('select * from Usuario where IdUsuario = ?', userid).fetchone()
            return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.delete("/user/{id_user}", tags=['Usuario'])
def delete_user(id_user: int):
    try:
        with conexion().cursor() as cursor:
            cursor.execute('exec DeleteUsuario @IdUsuario = ?', id_user)
        return {"message": "Usuario eliminado correctamente"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/ventas", tags=['Venta']) #FUNCIONA CUANDO QUIERE Y NO SÉ PQ -> ARREGLAR
def create_venta(iduser: int):
    try:    
        with conexion().cursor() as cursor:
            cursor.execute('exec CrearVenta @IdUsuario = ?', (iduser,))
            result = cursor.fetchone()
            print(result)
            if result:
                id_venta = result[0]
            else: 
                print("no hay id")
                raise HTTPException(status_code=500, detail="No se devolvió un IdVenta")
            conexion().commit()
        return {"message": "Venta creada exitosamente", "IdVenta": id_venta}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/detalle-venta", tags=['DetalleVenta']) #SÍ FUNCIONA
def add_detalle_venta(detventa: DetalleVenta):
    try:
        with conexion().cursor() as cursor: 
            cursor.execute('exec AgregarProductosDetalleVenta @IdVenta = ?, @IdProducto = ?, @Cantidad = ?', 
                           (detventa.IdVenta, detventa.IdProducto, detventa.Cantidad))
            conexion().commit()
        return {"message": "Producto agregado a detalle de venta exitosamente"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/venta/{id_venta}/actualizar-importes", tags=['Venta']) #CÓDIGO 200 SÍ FUNCIONA, FALTA VER EN LA TABLA DE LA BD
def update_importes(id_venta: int):
    try:
        with conexion().cursor() as cursor:
            cursor.execute("exec ActualizarImportesVenta @IdVenta = ?", (id_venta))
            conexion().commit()
        return {"message": "Importes de la venta actualizados exitosamente"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))