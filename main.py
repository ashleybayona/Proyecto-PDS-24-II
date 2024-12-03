#LIBRERIAS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from apscheduler.schedulers.background import BackgroundScheduler

#ARCHIVOS
from routers.users import users_router
from routers.products import products_router
from routers.payment import payment_router
from routers.billing import billing_router
from routers.billing_detail import billing_detail_router
from routers.login import login_router
from routers.entrega_scheduler import actualizar_entregas

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

scheduler = BackgroundScheduler()
scheduler.add_job(actualizar_entregas, 'interval', minutes=1)
scheduler.start()

@app.get("/", tags=['Home'])
def home():
    return "wasaaaa"

@app.on_event("shutdown")
async def shutdown_event():
    print("Apagando aplicación...")
    scheduler.shutdown() 

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)