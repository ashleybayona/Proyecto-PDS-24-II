#ARCHIVOS
from scheme_base.base_producto import *

class Producto(UpdateProducto):
    idProducto: int 
    idTipoProducto: int

class CreateProducto(UpdateProducto):
    tipoProducto: str
    idTipoProducto: int | None = None

'''
para crear: idtipo, nombre, descripcion, preciounit, imagen
para editar: nombre, descripcion, preciounit, imagen'''
