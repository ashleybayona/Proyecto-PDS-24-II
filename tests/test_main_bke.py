# test_main.py
from fastapi.testclient import TestClient
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "wasaaaa"

def test_get_productos():
    response = client.get("/productos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_usuarios():
    response = client.get("/usuarios")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_ventas():
    response = client.get("/ventas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_usuario():
    new_user = {
        "dni": "12345678",
        "nombre": "John",
        "apellido": "Doe",
        "telefono": "123456789",
        "email": "ashley.bayonav@gmail.com",
        "direccion": "123 Main St",
        "referencia": "Near Park",
        "passw": "password123"
    }
    response = client.post("/usuario", json=new_user)
    assert response.status_code == 200
    assert response.json() == {"message": "Usuario creado exitosamente"} #al crear le asignará el idusuario 6

def test_update_user():
    updated_user = {
        "telefono": "987654321",
        "email": "ashley.bayonav@gmail.com",
        "direccion": "456 Main St",
        "referencia": "Near School",
        "passw": "newpassword123"
    }
    response = client.put("/user/6", json=updated_user)
    assert response.status_code == 200
    assert "idUsuario" in response.json()

def test_delete_user():
    response = client.delete("/user/6")
    assert response.status_code == 200
    assert response.json() == {"message": "Usuario eliminado correctamente"}

def test_create_venta():
    response = client.post("/ventas", params={"iduser": 6})
    assert response.status_code == 200
    assert "IdVenta" in response.json() #al crear le asigna idventa 32

def test_add_detalle_venta():
    detalle_venta = {
        "idVenta": 32,
        "idProducto": 1,
        "cantidad": 2
    }
    response = client.post("/detalle-venta", json=detalle_venta)
    assert response.status_code == 200
    assert response.json() == {"message": "Producto agregado a detalle de venta exitosamente"}

def test_update_importes_venta():
    response = client.put("/venta/32/actualizar-importes")
    assert response.status_code == 200
    assert response.json() == {"message": "Importes de la venta actualizados exitosamente"}