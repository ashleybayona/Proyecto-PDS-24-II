import unittest
from fastapi.testclient import TestClient
from main import app  # Asegúrate de importar correctamente tu aplicación FastAPI desde el archivo donde está tu código.
from unittest.mock import patch

client = TestClient(app)

class TestAPI(unittest.TestCase):

    @patch('conexion_sqlserver.conexion')  # Cambiado aquí
    def test_get_productos(self, mock_conexion):
        # Configuramos el mock de la conexión y la ejecución del cursor
        mock_cursor = mock_conexion.return_value.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [
            {"IdProducto": 1, "Nombre": "Producto 1", "Precio": 100},
            {"IdProducto": 2, "Nombre": "Producto 2", "Precio": 200},
        ]

        response = client.get("/productos")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["Nombre"], "Producto 1")

    @patch('conexion_sqlserver.conexion')  # Cambiado aquí
    def test_get_usuarios(self, mock_conexion):
        # Configuramos el mock de la conexión y la ejecución del cursor
        mock_cursor = mock_conexion.return_value.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [
            {"IdUsuario": 1, "Nombre": "Juan", "Apellido": "Perez"},
            {"IdUsuario": 2, "Nombre": "Ana", "Apellido": "Lopez"},
        ]

        response = client.get("/usuarios")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["Nombre"], "Juan")

    @patch('conexion_sqlserver.conexion')  # Cambiado aquí
    def test_get_ventas(self, mock_conexion):
        # Configuramos el mock de la conexión y la ejecución del cursor
        mock_cursor = mock_conexion.return_value.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [
            {"IdVenta": 1, "Total": 150},
            {"IdVenta": 2, "Total": 300},
        ]

        response = client.get("/ventas")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["IdVenta"], 1)

    @patch('conexion_sqlserver.conexion')  # Cambiado aquí
    @patch('werkzeug.security.generate_password_hash')
    def test_create_usuario(self, mock_generate_password_hash, mock_conexion):
        # Configuramos el mock para la generación del hash de la contraseña
        mock_generate_password_hash.return_value = "hashed_password"
        # Configuramos el mock de la conexión
        mock_cursor = mock_conexion.return_value.cursor.return_value.__enter__.return_value

        # Simulamos el cuerpo de la petición
        usuario_data = {
            "DNI": "12345678",
            "Nombre": "Carlos",
            "Apellido": "Ramirez",
            "Telefono": "987654321",
            "Email": "carlos@example.com",
            "Direccion": "Av. Siempre Viva",
            "Referencia": "Cerca del parque",
            "Contrasenia": "mypassword"
        }

        response = client.post("/usuario", json=usuario_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["Nombre"], "Carlos")

    @patch('conexion_sqlserver.conexion')  # Cambiado aquí
    def test_create_venta(self, mock_conexion):
        # Configuramos el mock de la conexión y la ejecución del cursor
        mock_cursor = mock_conexion.return_value.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = [1]  # Simulamos que devuelve un IdVenta

        response = client.post("/ventas", params={"iduser": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["IdVenta"], 1)

    @patch('conexion_sqlserver.conexion')  # Cambiado aquí
    def test_add_detalle_venta(self, mock_conexion):
        # Configuramos el mock de la conexión y la ejecución del cursor
        mock_cursor = mock_conexion.return_value.cursor.return_value.__enter__.return_value

        # Simulamos el cuerpo de la petición
        detalle_venta_data = {
            "IdVenta": 1,
            "IdProducto": 1,
            "Cantidad": 3
        }

        response = client.post("/detalle-venta", json=detalle_venta_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Producto agregado a detalle de venta exitosamente")

    @patch('conexion_sqlserver.conexion')  # Cambiado aquí
    def test_update_importes(self, mock_conexion):
        # Configuramos el mock de la conexión y la ejecución del cursor
        mock_cursor = mock_conexion.return_value.cursor.return_value.__enter__.return_value

        response = client.put("/venta/1/actualizar-importes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Importes de la venta actualizados exitosamente")


if __name__ == '__main__':
    unittest.main()
