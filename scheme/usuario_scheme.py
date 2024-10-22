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

class UpdateUser(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None
    referencia: str | None = None
    passw: str | None = None