from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    IdUSuario: int
    IdTipoUsuario: int
    DNI: str
    Nombre: str
    Apellido: str
    Telefono: str
    Email: str
    Direccion: str
    Referencia: Optional[str]
    Constrasenia: str