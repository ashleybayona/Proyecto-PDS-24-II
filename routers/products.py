#LIBRERIAS
from fastapi import APIRouter, HTTPException
from typing import List

#ARCHIVOS
from config.connect_mysql import *
from scheme.productos_scheme import *

products_router = APIRouter()

#PARA VER TODOS LOS PRODUCTOS
@products_router.get("/productos", tags=['Producto'], response_model=List[Producto]) #funciona
def get_productos():
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute('select * from producto')
            productos = cursor.fetchall() 
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()


#TOO ESTO ES PARTE DEL ADMINISTRADOR
#AGREGAR PRODUCTO
@products_router.post("/producto", tags=['Producto'])
def create_producto(data: CreateProducto):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor() as cursor:
            new_product = data.dict()
            new_product['idTipoProducto'] = obtenerIdTipoProducto(new_product['tipoProducto'])
            cursor.callproc('crear_producto', [new_product['idTipoProducto'], new_product['nombreProducto'], new_product['descripcion'], new_product['precioUnitario'], new_product['imagen']])
            conexion.commit()
        return {"message": "Producto creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#EDITAR PRODUCTO
@products_router.put("/update-product/{id}", tags=['Producto'])
def update_product(data: UpdateProducto, id: int):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            cursor.callproc('update_producto', [id, data.nombreProducto, data.descripcion, data.precioUnitario, data.imagen])
            conexion.commit()

            if cursor.rowcount > 0:
                return {
                    "status": "success",
                    "message": "Producto actualizado correctamente"
                    }
            else:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"message": "Producto actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()

#ELIMINAR PRODUCTO
@products_router.delete("/delete-product/{id}", tags=['Producto'])
def delete_product(id: int):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor() as cursor:
            cursor.callproc('delete_producto', [id])
            conexion.commit()
        return {"message": "Producto eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()