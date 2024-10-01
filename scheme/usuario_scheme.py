from pydantic import BaseModel

class Usuario(BaseModel):
    IdUsuario: int | None = None
    IdTipoUsuario: int | None = None
    DNI: str
    Nombre: str
    Apellido: str
    Telefono: str
    Email: str
    Direccion: str
    Referencia: str | None = None
    Contrasenia: str