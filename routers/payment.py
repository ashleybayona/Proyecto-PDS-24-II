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
        #data = await request.json()
        #print(data)
        total = get_total(idventa)
        request = OrdersCreateRequest()

        request.prefer('return=representation')
        request.request_body(
            {
                'intent': 'CAPTURE',
                'purchase_units': [
                    {
                        'amount': {
                            'currency_code': 'USD',
                            'value': f'{total}'
                        }
                    }
                ],
                #'items': data
            }
        )
        response = client.execute(request)
        return JSONResponse(content={id: response.result.id })
    except IOError:
        print(IOError)
'''
@payment_router.post('/create-order/{idventa}')
async def create_order_paypal(idventa: int):
    try:
        total = get_total(idventa)
        request = OrdersCreateRequest()

        request.prefer('return=representation')
        request.request_body(
            {
                'intent': 'CAPTURE',
                'purchase_units': [
                    {
                        'amount': {
                            'currency_code': 'PEN',
                            'value': f'{total}'
                        }
                    }
                ],
                #'items': data
            }
        )
        response = client.execute(request)
        return JSONResponse(content={'id': response.result.id })
    except IOError:
        print(IOError)