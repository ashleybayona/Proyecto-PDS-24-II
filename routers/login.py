#LIBRERÍAS
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from werkzeug.security import check_password_hash 

#ARCHIVOS
from config.connect_mysql import *


login_router = APIRouter()

#TOKEN PARA VERIFICAR CORREO
#...

oauth2_scheme = OAuth2PasswordBearer("/token")

#LOGIN DE USUARIOS
@login_router.get("/users/me", tags=['Usuario']) #ESTE FALTA COMPLETAR
def read_users(token: str = Depends(oauth2_scheme)):
    return 'USER'

@login_router.post("/token", tags=['Usuario']) #FALTA MEJORAR
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        conexion = conexion_pool.get_connection()
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute('select * from usuario where email = %s and eliminado = 0', (form_data.username,))
            user = cursor.fetchone()
            if user:
                check_passw = check_password_hash(user['passw'], form_data.password)
                if check_passw:
                    '''acces_token_expires = timedelta(minutes=30)
                    acces_token_jwt = create_token()'''
                    return {
                        'message': 'Usuario logueado exitosamente',
                        'user_id': user['idUsuario']
                    }
                    '''{ #aka falla
                        "access_token": "gaaa",
                        "token_type": "bearer"
                    }'''
                else:
                    raise HTTPException(status_code=400, detail="Contraseña incorrecta")
            else:
                raise HTTPException(status_code=400, detail="Usuario no encontrado")           
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conexion.is_connected():
            conexion.close()