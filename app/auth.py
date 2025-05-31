# app/auth.py

from datetime import datetime, timedelta
from jose import JWTError, jwt

# Clave secreta para firmar los tokens (¡no compartir!)
SECRET_KEY = "clave_supersecreta_que_debes_cambiar"
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60

def crear_token(data: dict):
    to_encode = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=EXPIRACION_MINUTOS)
    to_encode.update({"exp": expira})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
