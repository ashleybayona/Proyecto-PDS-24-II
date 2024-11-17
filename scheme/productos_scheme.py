#ARCHIVOS
from scheme_base.base_producto import *

class Producto(UploadProducto):
    idProducto: int 
    idTipoProducto: int

class CreateProducto(UploadProducto):
    idTipoProducto: int

'''
para crear: idtipo, nombre, descripcion, preciounit, imagen
para editar: nombre, descripcion, preciounit, imagen'''