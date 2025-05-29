# app/routers/usuarios.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from .. import database, models
from fastapi import Path

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        rol="cliente"
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario registrado exitosamente."}

@router.post("/login")
def login(correo: str, contraseña: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()

    if not usuario or not bcrypt.verify(contraseña, usuario.contraseña):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")

    if usuario.estado != 'activo':
        raise HTTPException(status_code=403, detail="Usuario inactivo. Contacte a un administrador.")

    return {"mensaje": f"Bienvenido {usuario.nombre}", "rol": usuario.rol}


@router.put("/cambiar-rol/{usuario_id}")
def cambiar_rol(
    admin_id: int,
    nuevo_rol: str,
    usuario_id: int = Path(..., description="ID del usuario a modificar"),
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

@router.get("/")
def listar_usuarios(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(models.Usuario).filter(models.Usuario.id == admin_id, models.Usuario.rol == "admin").first()
    if not admin:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden ver la lista de usuarios.")

    usuarios = db.query(models.Usuario).all()
    return usuarios

@router.put("/cambiar-estado/{usuario_id}")
def cambiar_estado(
    admin_id: int,
    nuevo_estado: str,  # 'activo' o 'inactivo'
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



