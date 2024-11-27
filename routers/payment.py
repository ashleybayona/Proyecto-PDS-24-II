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
            print(productos)

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


'''#DE PRUEBA PARA VER Q RETORNA
@payment_router.post("/prueba-checkout-session")
def create_checkout_session(): 
    line_items = [
        {
            "price_data": {
                "currency": "PEN",
                "product_data": {
                    "name": "T-shirt",
                },
                "unit_amount": 2000,
            },
            "quantity": 1,
        },
        {
            "price_data": {
                "currency": "PEN",
                "product_data": {
                    "name": "africano",
                },
                "unit_amount": 5000,
            },
            "quantity": 3,
        },
    ]

    try:
        #se crea la sesión en stripe
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="https://z2rvnq4d-5173.brs.devtunnels.ms/", #CAMBIAR
            cancel_url="https://z2rvnq4d-5173.brs.devtunnels.ms/cancel", #CAMBIAR
        )
        print(session)
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creando sesión de pago: {str(e)}")'''

@payment_router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    print("entra")
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    print("2entraa")

    try:
        # Verifica que el evento provenga de Stripe
        event = Webhook.construct_event(payload, sig_header, webhook_key)
        print(event)

    except ValueError as e:
        # Error en el payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except SignatureVerificationError as e:
        # Error en la firma
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Maneja el evento del pago
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(session)

        # Recupera datos del usuario desde metadata
        idUsuario = int(session["metadata"]["idUsuario"])
        print("idUsuario", idUsuario)

        # Guarda la información en la base de datos
        try:
            await guardarCompra(idUsuario, session)
        except HTTPException as e:
            print(f"Error al guardar la compra: {str(e)}")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")

    return {"status": "success"}

''' print(event)
{
    "api_version": "2024-10-28.acacia",
    "created": 1732670920,
    "data": {
        "object": {
            "adaptive_pricing": {
                "enabled": false
            },
            "after_expiration": null,
            "allow_promotion_codes": null,
            "amount_subtotal": 8700,
            "amount_total": 8700, #MONTO TOTAL AKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            "automatic_tax": {
                "enabled": false,
                "liability": null,
                "status": null
            },
            "billing_address_collection": null,
            "cancel_url": "https://z2rvnq4d-5173.brs.devtunnels.ms/cancel";,
            "client_reference_id": null,
            "client_secret": null,
            "consent": null,
            "consent_collection": null,
            "created": 1732670879,
            "currency": "pen",
            "currency_conversion": null,
            "custom_fields": [],
            "custom_text": {
                "after_submit": null,
                "shipping_address": null,
                "submit": null,
                "terms_of_service_acceptance": null
            },
            "customer": null,
            "customer_creation": "if_required",
            "customer_details": {
                "address": {
                    "city": null,
                    "country": "PE",
                    "line1": null,
                    "line2": null,
                    "postal_code": null,
                    "state": null
                },
                "email": "sm.lapuntita@gmail.com",
                "name": "la puntita",
                "phone": null,
                "tax_exempt": "none",
                "tax_ids": []
            },
            "customer_email": null,
            "expires_at": 1732757279,
            "id": "cs_test_b1d1bAro1bNPCgpv4XBmQwIsgeJZCUPuYaxWpyfNSLm640EeBbjMkQfVQT",
            "invoice": null,
            "invoice_creation": {
                "enabled": false,
                "invoice_data": {
                    "account_tax_ids": null,
                    "custom_fields": null,
                    "description": null,
                    "footer": null,
                    "issuer": null,
                    "metadata": {},
                    "rendering_options": null
                }
            },
            "livemode": false,
            "locale": null,
            "metadata": {
                "idUsuario": "1"
            },
            "mode": "payment",
            "object": "checkout.session",
            "payment_intent": "pi_3QPa3W07GBSgIitx0Zf71b19",
            "payment_link": null,
            "payment_method_collection": "if_required",
            "payment_method_configuration_details": null,
            "payment_method_options": {
                "card": {
                    "request_three_d_secure": "automatic"
                }
            },
            "payment_method_types": [
                "card"
            ],
            "payment_status": "paid", #ESTADO DE PAGO AKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            "phone_number_collection": {
                "enabled": false
            },
            "recovered_from": null,
            "saved_payment_method_options": null,
            "setup_intent": null,
            "shipping_address_collection": null,
            "shipping_cost": null,
            "shipping_details": null,
            "shipping_options": [],
            "status": "complete",
            "submit_type": null,
            "subscription": null,
            "success_url": "https://z2rvnq4d-5173.brs.devtunnels.ms/";,
            "total_details": {
                "amount_discount": 0,
                "amount_shipping": 0,
                "amount_tax": 0
            },
            "ui_mode": "hosted",
            "url": null
        }
    },
    "id": "evt_1QPa3Y07GBSgIitxGGEz1Kbs",
    "livemode": false,
    "object": "event",
    "pending_webhooks": 1,
    "request": {
        "id": null,
        "idempotency_key": null
    },
    "type": "checkout.session.completed"
}
'''