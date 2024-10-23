from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    idUsuario: int | None = None
    idTipoUsuario: int | None = None
    dni: str
    nombre: str
    apellido: str
    telefono: str
    email: str
    direccion: str
    referencia: str | None = None
    passw: str
    correoVerificado: int | None = 0

class UpdateUser(BaseModel):
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None
    referencia: str | None = None
    passw: str | None = None