#LIBRERÍAS 
from stripe import stripe
from stripe.error import SignatureVerificationError
from stripe.webhook import Webhook
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import json
import os 
from dotenv import load_dotenv

#ARCHIVOS
from scheme.facturacion_scheme import *
from config.connect_mysql import *

payment_router = APIRouter()

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
webhook_key = os.getenv("WEBHOOK_KEY")

'''FLUJO DE VENTA CON CARRITO DE COMPRA INCLUYENDO DELIVERY
el frontend pasa en formato json el idusuer, idproduct y la cantidad de los productos, también el monto de delivery, en el backend se hace el cálculo de los precios y se envía a stripe para que genere el checkout session, el cual se envía al frontend para que redirija al usuario a la página de pago de stripe, una vez que el usuario paga, stripe envía una notificación al backend para que se actualice el estado de la orden, guardándose los datos recién en la base de datos y se envía un correo al usuario con la confirmación de la compra.

{
    "idUsuario": 9,
    "productos":[
        {"idProducto": 21, "cantidad": 1}, 
        {"idProducto": 27, "cantidad": 1}
    ],
    "delivery": 0,
    "tipoDocumento": "boleta"
}
'''

#este solo solicita el pago, si se completa recién guarda la info en la base de datos
@payment_router.post("/create-checkout-session") #funciona
def create_checkout_session(data: dict): #idUsuario, productos(idProducto, cantidad), impDelivery, tipoDocumento
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            iduser = data["idUsuario"]
            productos = data["productos"]
            impdelivery = data["delivery"]
            tipoDocumento = data["tipoDocumento"]

            #precioTotalProductos, igv, productosCalculados
            subtotal, igv, productosCalculados = calcularImportes(productos, cursor) #esto puede solo devolver el diccionario de productosCalculados y no lo demas, revisar
            total = subtotal + igv + impdelivery

            line_items = [
                {
                    "price_data": {
                        "currency": "pen",
                        "product_data": {"name": producto["nombreProducto"]},
                        "unit_amount": int(producto["precioUnitario"] * 100),
                    },
                    "quantity": producto["cantidad"],
                }
                for producto in productosCalculados
            ]

            if impdelivery > 0:
                line_items.append({
                    "price_data": {
                        "currency": "pen",
                        "product_data": {"name": "Costo de Delivery"},
                        "unit_amount": int(impdelivery * 100),
                    },
                    "quantity": 1,
                })

            try:
                #se crea la sesión en stripe
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=line_items,
                    mode="payment",
                    success_url="https://web.facebook.com/?_rdc=1&_rdr", #CAMBIAR
                    cancel_url="https://z2rvnq4d-5173.brs.devtunnels.ms/cancel", #CAMBIAR
                    metadata={ # metadata solo acepta strings
                        "idUsuario": str(iduser),
                        "productos": json.dumps(productos),
                        "impVenta": str(subtotal),
                        "impDelivery": str(impdelivery),
                        "impIGV": str(igv),
                        "impTotal": str(total),
                        "tipoDocumento": tipoDocumento 
                    },
                )
                return {"url": session.url}
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error creando sesión de pago: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creando sesión de pago: {str(e)}")
    finally:
        if conexion.is_connected():
            conexion.close()


'''#DE PRUEBA
{
    "idUsuario": 9,
    "productos":[
        {"idProducto": 3, "cantidad": 1}, 
        {"idProducto": 10, "cantidad": 1},
        {"idProducto": 36, "cantidad": 1}
    ],
    "delivery": 5,
    "tipoDocumento": "boleta"
}'''

#entra cuando se completa el pago, si esta para delivery se debe de guardar en la tabla de entrega y debe de asignarse un repartidor de forma aleatoria con tal que esté disponible y luego ese reparitdor debe de cambiar su estado a ocupado
@payment_router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        # Verifica que el evento provenga de Stripe
        event = Webhook.construct_event(payload, sig_header, webhook_key)

    except ValueError as e:
        # Error en el payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except SignatureVerificationError as e:
        # Error en la firma
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Maneja el evento del pago
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Recupera datos del usuario desde metadata
        idUsuario = int(session["metadata"]["idUsuario"])

        # Guarda la información en la base de datos
        try:
            await guardarCompra(idUsuario, session)
        except HTTPException as e:
            print(f"Error al guardar la compra: {str(e)}")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")

    return {"status": "success"}

