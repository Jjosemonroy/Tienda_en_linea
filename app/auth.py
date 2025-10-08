# app/auth.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Header

load_dotenv()

# Clave secreta para firmar los tokens (¡no compartir!)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "clave_supersecreta_que_debes_cambiar")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRACION_MINUTOS = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))

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

# Dependencia para proteger endpoints
async def get_current_user(authorization: str = Header(...)):
    esquema, _, token = authorization.partition(" ")
    if esquema.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Token de autenticación inválido o ausente")
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return payload
