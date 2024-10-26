# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#falta ver como llevar lo de eliminar usuario si se eliminan tmb las filas en las tablas relacionadas(venta, detalleventa) con un trigger o hacer q 

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
    n_user = {
        "telefono": "976547982",
        "email": "ashley.bayonav@gmail.com",
        "direccion": "123 Main St",
        "referencia": "Near Park",
        "passw": "password123",
        "dni": "12345678",
        "nombre": "John",
        "apellido": "Doe"
    }
    response = client.post("/usuario", json=n_user)
    print(response)
    assert response.status_code == 200
    assert response.json() == {"message": "Usuario creado exitosamente"} #al crear le asignará el idusuario 8

def test_update_user():
    updated_user = {
        "telefono": "987654321",
        "email": "ashley.bayonav@gmail.com",
        "direccion": "456 Main St",
        "referencia": "Near School",
        "passw": "newpassword123"
    }
    response = client.put("/user/8", json=updated_user)
    assert response.status_code == 200
    assert "idUsuario" in response.json()

def test_create_venta():
    response = client.post("/ventas", params={"iduser": 8})
    assert response.status_code == 200
    assert "IdVenta" in response.json() #al crear le asigna idventa 53

def test_add_detalle_venta():
    detalle_venta = {
        "idVenta": 53,
        "idProducto": 1,
        "cantidad": 2
    }
    response = client.post("/detalle-venta", json=detalle_venta)
    assert response.status_code == 200
    assert response.json() == {"message": "Producto agregado a detalle de venta exitosamente"}

def test_update_importes_venta():
    response = client.put("/venta/53/actualizar-importes")
    assert response.status_code == 200
    assert response.json() == {"message": "Importes de la venta actualizados exitosamente"}

def test_delete_user():
    response = client.delete("/user/8")
    assert response.status_code == 200
    assert response.json() == {"message": "Usuario eliminado correctamente"}