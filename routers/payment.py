#LIBRERÍAS 
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest
from os import getenv
from dotenv import load_dotenv

#ARCHIVOS
from scheme_base.base_venta import *

payment_router = APIRouter()

load_dotenv()

#Acces Token for SandBox
client_id = getenv('CLIENT_ID')
client_secret = getenv('CLIENT_SECRET')

#Creating an environment
environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment)

#OBTENER EL ORDER ID DE PAYPAL
'''@payment_router.post('/create-order/{idventa}')
async def create_order_paypal(idventa: int, request: Request):
    try:
        data = await request.json() #items de la compra -> ESTO TMB SE PUEDE HACER CON PROCEDIMIENTO ALMACENADO
        total = get_total(idventa)
        value = f"{total:.2f}" 

        request = OrdersCreateRequest()

        request.prefer('return=representation')
        request.request_body(
            {
                'intent': 'CAPTURE',
                'purchase_units': [
                    {
                        'amount': {
                            'currency_code': 'USD', #ESTO DEBE DE SER CAMBIADO A PEN, PERO NO SE PUEDE POR EL MOMENTO
                            'value': value
                        }
                    }
                ],
                'items': data
            }
        )
        response = client.execute(request)
        #FALTA AGREGAR Q EL ID SE GUARDE EN LA BD
        return JSONResponse(content={id: response.result.id })
    except IOError:
        print(IOError)'''


#PRUEBA DEL ENDPOINT SIN REQUEST DEL FRONT
@payment_router.post('/create-order/{idventa}')
def create_order_paypal(idventa: int):
    try:
        total = get_total(idventa)
        value = f"{total:.2f}"  # Convierte total a string con dos decimales
        request = OrdersCreateRequest()

        request.prefer('return=representation')
        print('antes d request body')
        request.request_body(
            {
                'intent': 'CAPTURE',
                'purchase_units': [
                    {
                        'amount': {
                            'currency_code': 'USD',
                            'value': value
                        }
                    }
                ],
                #'items': data
            }
        ) 
        print(request)
        response = client.execute(request)
        print('despues de response')
        return JSONResponse(content={'id': response.result.id })
    except Exception as e:
        print(e)
        return JSONResponse(content={'error': 'Error al crear el pedido'})