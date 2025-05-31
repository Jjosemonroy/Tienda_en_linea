from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from typing import Optional
from .. import database, models
from ..auth import crear_token, verificar_token
from fastapi import Header

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

# Registro de usuario
@router.post("/registrar")
def registrar_usuario(nombre: str, correo: str, contraseña: str, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    contraseña_hash = bcrypt.hash(contraseña)
    nuevo_usuario = models.Usuario(
        nombre=nombre,
        correo=correo,
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
def login(correo: str, contraseña: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()

    if not usuario or not bcrypt.verify(contraseña, usuario.contraseña):
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
            "rol": usuario.rol
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
    admin_id: int,
    nuevo_rol: str,
    usuario_id: int = Path(...),
    db: Session = Depends(get_db)
):
    if nuevo_rol not in ["cliente", "admin"]:
        raise HTTPException(status_code=400, detail="Rol inválido. Usa 'cliente' o 'admin'.")

    admin = db.query(models.Usuario).filter(models.Usuario.id == admin_id, models.Usuario.rol == "admin").first()
    if not admin:
        raise HTTPException(status_code=403, detail="No tiene permisos para cambiar roles.")

    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.rol == nuevo_rol:
        return {"mensaje": f"El usuario ya tiene el rol '{nuevo_rol}'."}

    usuario.rol = nuevo_rol
    db.commit()
    return {"mensaje": f"El rol del usuario con ID {usuario.id} ahora es '{nuevo_rol}'"}

# Cambiar estado (activo/inactivo)
@router.put("/cambiar-estado/{usuario_id}")
def cambiar_estado(
    admin_id: int,
    nuevo_estado: str,
    usuario_id: int,
    db: Session = Depends(get_db)
):
    if nuevo_estado not in ["activo", "inactivo"]:
        raise HTTPException(status_code=400, detail="Estado inválido. Usa 'activo' o 'inactivo'.")

    admin = db.query(models.Usuario).filter(models.Usuario.id == admin_id, models.Usuario.rol == "admin").first()
    if not admin:
        raise HTTPException(status_code=403, detail="No tiene permisos para cambiar estado.")

    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.estado = nuevo_estado
    db.commit()
    return {"mensaje": f"El usuario ahora está '{nuevo_estado}'"}
