from pydantic import EmailStr, validator
from scheme_base.base_usuario import *

class Usuario(BaseUsuario): #este solo se usa para mostrar los atributos
    idUsuario: int 
    tipoUsuario: str #enum
    dni: str
    nombre: str
    apellido: str
    correoVerificado: str #enum
    eliminado: str #enum

class CreateUser(BaseUsuario):
    dni: str
    nombre: str
    apellido: str

    #validar dni: que se ingresen números y la longitud sea de 8 (solo perú)
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