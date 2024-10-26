'''import phonenumbers

x = phonenumbers.parse('912345678', 'PE')
print(x.country_code) #51 codigo pais
print(x.country_code_source) #0
print(x.extension) #none
print(x.national_number) #num ingresado
print(phonenumbers.is_valid_number(x)) #true or false
'''

from pydantic import EmailStr, BaseModel

class user(BaseModel):
    email: EmailStr

    def validar(email):
        if email:
            print('si')

hola = user(email='ashley.bayonav@gmail.com')
hola.validar()