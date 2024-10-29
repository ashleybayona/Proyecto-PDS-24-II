from pydantic import EmailStr, validator
from scheme_base.base_usuario import *

class Usuario(BaseUsuario):
    idUsuario: int | None = None
    idTipoUsuario: int | None = None
    dni: str
    nombre: str
    apellido: str
    correoVerificado: int | None = 0
    eliminado: int | None = 0

class CreateUser(BaseUsuario):
    dni: str
    nombre: str
    apellido: str

    #validar dni
    @validator('dni')
    def validar_dni(cls, num):
        if not (num.isdigit() and len(num) == 8):
            raise ValueError('El DNI debe tener exactamente 8 dígitos')
        return num

class UpdateUser(BaseUsuario):
    telefono: str | None = None
    email: EmailStr | None = None
    direccion: str | None = None
    referencia: str | None = None
    passw: str | None = None