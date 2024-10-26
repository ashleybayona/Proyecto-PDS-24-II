#archivo donde se harán las validaciones en la clase principal para que luego se hereden
from pydantic import BaseModel, EmailStr, validator
import phonenumbers
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

API_MAIL_KEY = os.getenv('API_MAIL_KEY')

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
    ✅ email si existe, servicios de terceros, cada 1 permite 100 requests: hunter.io, zerobounce, mailboxlayer (emailstr solo valida si está en el formato correcto)
    ✅ contraseña con mínimo 6 de len
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

    #validar contraseña
    @validator('passw')
    def validar_passw(cls, password):
        if len(password) < 6:
            raise ValueError('La contraseña debe tener al menos 6 carácteres')
        return password

#validar email
async def validar_email(mail):
    url = "https://api.hunter.io/v2/email-verifier"
    params = {
        'email': mail,
        'key': API_MAIL_KEY
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

        status = data['data']['status'] #tiene que ser webmail o valid
        result = data['data']['result'] #tiene que ser deliverable 

        if status in ['valid', 'webmail'] and result == 'deliverable':
            return True
        return False