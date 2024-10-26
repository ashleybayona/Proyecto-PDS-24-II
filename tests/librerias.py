#ARCHIVO PARA PROBAR LIBRERIAS O ERRORES EN MENOS CODIGO (NO FUNDAMENTAL PARA EL PROYECTO)
'''import phonenumbers

x = phonenumbers.parse('912345678', 'PE')
print(x.country_code) #51 codigo pais
print(x.country_code_source) #0
print(x.extension) #none
print(x.national_number) #num ingresado
print(phonenumbers.is_valid_number(x)) #true or false
'''

from pydantic import EmailStr, BaseModel
import httpx
import asyncio 

class user(BaseModel):
    email: EmailStr

    def validar(email):
        if email:
            print('si')

hola = user(email='ashley.bayonav@gmail.com')
print(hola)
print(hola.email)
hola.validar()

holadict = hola.dict()
print(holadict)
print(holadict['email'])

async def validar_email(mail):
    url = "https://api.hunter.io/v2/email-verifier"
    params = {
        'email': mail,
        'api_key': 'c6ff6c154ca5621cad1b02d3b644c46a2aa9f811'
    }
    print('antes de await')
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        print('despues de await')
        print(data)

        status = data['data']['status'] #tiene que ser webmail o valid
        result = data['data']['result'] #tiene que ser deliverable 

        print(status)
        print(result)

        if status in ['valid', 'webmail'] and result == 'deliverable':
            print('ci')
            return True
        return False

def otra_funcion(data: user):
    holadict = data.dict()
    valid = asyncio.run(validar_email(holadict['email'])) 
    print(valid)

otra_funcion(hola)