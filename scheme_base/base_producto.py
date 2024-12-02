from pydantic import BaseModel

class UpdateProducto(BaseModel):
    nombreProducto: str | None = None
    descripcion: str | None = None
    precioUnitario: float | None = None
    imagen: str | None = None

#en el dic se guarda con el nombre del tipo de producto pero debe de haber una funcion que pase ese nombre al numero del id tipo producto para que se guarde en la base de datos
def obtenerIdTipoProducto(tipo: str):
    tipo = tipo.lower()
    if tipo == 'alimento':
        return 1
    elif tipo == 'bebida':
        return 2
    elif tipo == 'topping':
        return 3
    elif tipo == 'promo':
        return 4