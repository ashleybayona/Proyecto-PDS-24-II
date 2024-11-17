from pydantic import BaseModel
from datetime import datetime


class Facturacion(BaseModel):
    idFacturacion: int 
    idUsuario: int
    importeVenta: float 
    importeDelivery: float 
    importeIGV: float 
    importeTotal: float
    fecha: datetime 
    codigoBoleta: str 
    tipoDocumento: str
    idStripe: str | None = 0
    estadoPago: str 

def calcularImportes(productos, cursor): #devuelve importeVenta, importeIGV / productos: {idProducto, cantidad}
    subtotal = 0.00
    productosCalculados = []

    for producto in productos:
        print(producto) #{'idProducto': 24, 'cantidad': 2}
        cursor.execute("select precioUnitario, nombreProducto from producto where idProducto = %s", [producto["idProducto"],]) 
        result = cursor.fetchone()  #result = {'precioUnitario': Decimal('16.00')}

        if not result: 
            raise ValueError(f"Producto {producto['idProducto']} no encontrado")
        
        #establece los montos de los productos
        producto["nombreProducto"] = result['nombreProducto']
        preciounit =  float(result['precioUnitario'])
        producto["precioUnitario"] = preciounit
        producto["precio"] = preciounit * producto["cantidad"]
        subtotal += producto["precio"]

        productosCalculados.append(producto)
    
    #modificado para que salgan los precios esperados 0.18 * PRECIO + PRECIO = PRECIO TOTAL
    precioTotalProductos = subtotal / 1.18 
    igv = precioTotalProductos * 0.18

    return precioTotalProductos, igv, productosCalculados
