#archivo donde se harán las validaciones en la clase principal para que luego se hereden
from pydantic import BaseModel, EmailStr, validator
import phonenumbers

class BaseUsuario(BaseModel):
    telefono: str
    email: EmailStr
    direccion: str 
    referencia: str | None = None
    passw: str 

    '''
    VALIDACIONES:
    ✅ número telefono sea de 9 dígitos (solo se toma en cuenta perú) formato perú 
    ✅ número de dni 8 dígitos (solo perú) ESTO IRÁ SOLO EN LA CLASE CREATEUSER
    - email si existe, servicios de terceros, cada 1 permite 100 requests: hunter.io, zerobounce, mailboxlayer (emailstr solo valida si está en el formato correcto)
    '''

    #validar telefono
    @validator('telefono')
    def validar_telefono(cls, num):
        if num:
            try:
                telef = phonenumbers.parse(num, 'PE')
                if not phonenumbers.is_valid_number(telef):
                    raise ValueError('Número de teléfono no válido con el formato PE')
            except phonenumbers.NumberParseException:
                raise ValueError('Número de teléfono no válido')
        return num
    
    #validar email