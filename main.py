from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyodbc

app = FastAPI()

#http://127.0.0.1:8000

# Modelo de datos para reservas
class Reserva(BaseModel):
    id: int
    nombre: str
    fecha: str

# Conexión a la base de datos
def get_db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=your_server_name;'
        'DATABASE=your_database_name;'
        'UID=your_username;'
        'PWD=your_password'
    )
    return connection

# Endpoint para obtener todas las reservas
@app.get("/reservas/")
def read_reservas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, fecha FROM reservas")
    reservas = cursor.fetchall()
    conn.close()
    return reservas

# Endpoint para crear una nueva reserva
@app.post("/reservas/")
def create_reserva(reserva: Reserva):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reservas (id, nombre, fecha) VALUES (?, ?, ?)",
                   (reserva.id, reserva.nombre, reserva.fecha))
    conn.commit()
    conn.close()
    return {"message": "Reserva creada exitosamente"}

# Endpoint para actualizar una reserva existente
@app.put("/reservas/{reserva_id}")
def update_reserva(reserva_id: int, reserva: Reserva):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE reservas SET nombre = ?, fecha = ? WHERE id = ?",
                   (reserva.nombre, reserva.fecha, reserva_id))
    conn.commit()
    conn.close()
    return {"message": "Reserva actualizada exitosamente"}

# Endpoint para eliminar una reserva
@app.delete("/reservas/{reserva_id}")
def delete_reserva(reserva_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservas WHERE id = ?", (reserva_id,))
    conn.commit()
    conn.close()
    return {"message": "Reserva eliminada exitosamente"}
