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

class UpdateUser(BaseModel):
    Nombre: str | None = None
    Apellido: str | None = None
    Telefono: str | None = None
    Email: str | None = None
    Direccion: str | None = None
    Referencia: str | None = None
    Contrasenia: str | None = None