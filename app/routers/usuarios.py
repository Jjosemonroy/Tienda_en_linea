from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from typing import Optional
from .. import database, models
from ..auth import crear_token, verificar_token
from fastapi import Header
from pydantic import BaseModel, EmailStr, constr

class RegistroUsuarioRequest(BaseModel):
    nombre: constr(strip_whitespace=True, min_length=2, max_length=100)
    correo: EmailStr
    contraseña: constr(min_length=8, max_length=64)

class LoginRequest(BaseModel):
    correo: EmailStr
    contraseña: constr(min_length=8, max_length=64)

class ChangePasswordRequest(BaseModel):
    correo: EmailStr
    contraseña_actual: constr(min_length=8, max_length=64)
    nueva_contraseña: constr(min_length=8, max_length=64)

class RestablecerContraseñaRequest(BaseModel):
    admin_id: int
    correo: EmailStr
    nueva_contraseña: constr(min_length=8, max_length=64)

class CambiarRolRequest(BaseModel):
    admin_id: int
    nuevo_rol: constr(strip_whitespace=True)

class CambiarEstadoRequest(BaseModel):
    admin_id: int
    nuevo_estado: constr(strip_whitespace=True)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependencia para extraer el usuario desde el token
def obtener_usuario_actual(authorization: str = Header(...)):
    esquema, _, token = authorization.partition(" ")
    if esquema.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Formato de autorización inválido")

    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return payload

# Registro de usuario con validación robusta
@router.post("/registrar")
def registrar_usuario(request: RegistroUsuarioRequest, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.correo == request.correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    contraseña_hash = bcrypt.hash(request.contraseña)
    nuevo_usuario = models.Usuario(
        nombre=request.nombre,
        correo=request.correo,
        contraseña=contraseña_hash,
        rol="cliente",
        estado="activo"
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario registrado exitosamente."}

# Login de usuario con generación de token
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == request.correo).first()

    if not usuario or not bcrypt.verify(request.contraseña, usuario.contraseña):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    if usuario.estado != 'activo':
        raise HTTPException(status_code=403, detail="Usuario inactivo. Contacte a un administrador.")

    token = crear_token({"sub": usuario.correo, "id": usuario.id, "rol": usuario.rol})

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rol": usuario.rol,
            "estado": usuario.estado
        }
    }

# Obtener listado de usuarios (solo admin)
@router.get("/")
def listar_usuarios(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(models.Usuario).filter(models.Usuario.id == admin_id, models.Usuario.rol == "admin").first()
    if not admin:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden ver la lista de usuarios.")

    usuarios = db.query(models.Usuario).all()
    return usuarios

# Cambiar rol (cliente ↔ admin)
@router.put("/cambiar-rol/{usuario_id}")
def cambiar_rol(
    usuario_id: int = Path(...),
    datos: CambiarRolRequest = Body(...),
    db: Session = Depends(get_db)
):
    if datos.nuevo_rol not in ["cliente", "admin"]:
        raise HTTPException(status_code=400, detail="Rol inválido. Usa 'cliente' o 'admin'.")

    admin = db.query(models.Usuario).filter(models.Usuario.id == datos.admin_id, models.Usuario.rol == "admin").first()
    if not admin:
        raise HTTPException(status_code=403, detail="No tiene permisos para cambiar roles.")

    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.rol == datos.nuevo_rol:
        return {"mensaje": f"El usuario ya tiene el rol '{datos.nuevo_rol}'."}

    usuario.rol = datos.nuevo_rol
    db.commit()
    return {"mensaje": f"El rol del usuario con ID {usuario.id} ahora es '{datos.nuevo_rol}'"}

# Cambiar estado (activo/inactivo)
@router.put("/cambiar-estado/{usuario_id}")
def cambiar_estado(
    usuario_id: int,
    datos: CambiarEstadoRequest = Body(...),
    db: Session = Depends(get_db)
):
    if datos.nuevo_estado not in ["activo", "inactivo"]:
        raise HTTPException(status_code=400, detail="Estado inválido. Usa 'activo' o 'inactivo'.")

    admin = db.query(models.Usuario).filter(models.Usuario.id == datos.admin_id, models.Usuario.rol == "admin").first()
    if not admin:
        raise HTTPException(status_code=403, detail="No tiene permisos para cambiar estado.")

    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.estado = datos.nuevo_estado
    db.commit()
    return {"mensaje": f"El usuario ahora está '{datos.nuevo_estado}'"}

@router.put("/cambiar-contraseña")
def cambiar_contraseña(
    datos: ChangePasswordRequest,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == datos.correo).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not bcrypt.verify(datos.contraseña_actual, usuario.contraseña):
        raise HTTPException(status_code=401, detail="Contraseña actual incorrecta")

    usuario.contraseña = bcrypt.hash(datos.nueva_contraseña)
    db.commit()

    return {"mensaje": "Contraseña actualizada correctamente"}

@router.put("/restablecer-contraseña")
def restablecer_contraseña(
    datos: RestablecerContraseñaRequest,
    db: Session = Depends(get_db)
):
    admin = db.query(models.Usuario).filter(models.Usuario.id == datos.admin_id).first()
    if not admin or admin.rol !="admin":
        raise HTTPException(status_code=403, detail="No tiene permisos para restablecer contraseñas.")
    
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == datos.correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.contraseña = bcrypt.hash(datos.nueva_contraseña)
    db.commit()

    return {"mensaje": f"Contraseña restablecida para {usuario.nombre}"}

