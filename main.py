#LIBRERIAS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

#ARCHIVOS
from routers.users import users_router
from routers.products import products_router
from routers.payment import payment_router
from routers.billing import billing_router
from routers.billing_detail import billing_detail_router
from routers.login import login_router

app = FastAPI()

app.include_router(users_router) #usuarios
app.include_router(products_router) #productos
app.include_router(payment_router) #pagos
app.include_router(billing_router) #facturación
app.include_router(billing_detail_router) #detalle de facturación
app.include_router(login_router) #login

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.title = 'API La Puntita' 

@app.get("/", tags=['Home'])
def home():
    return "wasaaaa"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)