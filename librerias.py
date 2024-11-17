#ARCHIVO PARA PROBAR LIBRERIAS O ERRORES EN MENOS CODIGO (NO FUNDAMENTAL PARA EL PROYECTO)
from config.connect_mysql import *

def prueba_importes(productos):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            #codigo de prueba
            subtotal = 0.00
            productosCalculados = []

            for producto in productos:
                print(producto) #{'idProducto': 24, 'cantidad': 2}
                cursor.execute("select precioUnitario, nombreProducto from producto where idProducto = %s", [producto["idProducto"],]) 
                result = cursor.fetchone()  #result = {'precioUnitario': Decimal('16.00')}

                if not result: 
                    raise ValueError(f"Producto {producto['idProducto']} no encontrado")
                
                #establece los montos de los productos
                nombre = result['nombreProducto']
                print(nombre)
                preciounit =  float(result['precioUnitario'])
                producto["precioUnitario"] = preciounit
                producto["precio"] = preciounit * producto["cantidad"]
                subtotal += producto["precio"]

                productosCalculados.append(producto)
                print(productosCalculados)
            
            #modificado para que salgan los precios esperados 0.18 * PRECIO + PRECIO = PRECIO TOTAL
            precioTotalProductos = subtotal / 1.18 
            igv = precioTotalProductos * 0.18
            print(subtotal)
            print(igv + precioTotalProductos)

            return precioTotalProductos, igv, productosCalculados
    except Exception as e:
        print(f"error en prueba: {e}")
    finally:
        if conexion.is_connected():
            conexion.close()

productos = [{"idProducto": 24, "cantidad": 2}, {"idProducto": 35, "cantidad": 3}]
prueba_importes(productos)



'''import phonenumbers

x = phonenumbers.parse('912345678', 'PE')
print(x.country_code) #51 codigo pais
print(x.country_code_source) #0
print(x.extension) #none
print(x.national_number) #num ingresado
print(phonenumbers.is_valid_number(x)) #true or false
'''

'''from pydantic import EmailStr, BaseModel
import httpx
import asyncio 
import os
from dotenv import load_dotenv
load_dotenv()

API_MAIL_KEY = os.getenv('API_MAIL_KEY')

class user(BaseModel):
    email: EmailStr

    def validar(email):
        if email:
            print('si')

hola = user(email='ashley.bayonav@gmail.com')
print(hola)
print(hola.email)
hola.validar()

holadict = hola.dict()
print(holadict)
print(holadict['email'])

async def validar_email(mail):
    url = "https://api.hunter.io/v2/email-verifier"
    params = {
        'email': mail,
        'api_key': API_MAIL_KEY
    }
    print('antes de await')
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        print('despues de await')
        print(data)

        status = data['data']['status'] #tiene que ser webmail o valid
        result = data['data']['result'] #tiene que ser deliverable 

        print(status)
        print(result)

        if status in ['valid', 'webmail'] and result == 'deliverable':
            print('ci')
            return True
        return False

def otra_funcion(data: user):
    holadict = data.dict()
    valid = asyncio.run(validar_email(holadict['email'])) 
    print(valid)

otra_funcion(hola)'''