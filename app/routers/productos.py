from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from .. import database, models
import os
import shutil
from uuid import uuid4

router = APIRouter(prefix="/productos", tags=["Productos"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear producto (solo admin)
@router.post("/")
def crear_producto(
    admin_id: int = Form(...),
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validar si es administrador
    admin = db.query(models.Usuario).filter(
        models.Usuario.id == admin_id,
        models.Usuario.rol == "admin"
    ).first()

    if not admin:
        raise HTTPException(status_code=403, detail="No tiene permisos para crear productos.")

    # Guardar imagen en carpeta local
    extension = os.path.splitext(imagen.filename)[1]
    filename = f"{uuid4().hex}{extension}"
    ruta_carpeta = "static/imagenes"
    os.makedirs(ruta_carpeta, exist_ok=True)
    ruta_imagen = os.path.join(ruta_carpeta, filename)

    with open(ruta_imagen, "wb") as buffer:
        shutil.copyfileobj(imagen.file, buffer)

    # Registrar producto
    nuevo_producto = models.Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock,
        imagen=f"/{ruta_imagen.replace(os.sep, '/')}"  # Ruta que será accesible vía http://localhost:8000/static/imagenes/...
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return {"mensaje": "Producto creado exitosamente", "producto": nuevo_producto.id}

# Listar productos (disponible para todos)
@router.get("/")
def listar_productos(db: Session = Depends(get_db)):
    productos = db.query(models.Producto).all()
    return productos

# Obtener producto por ID
@router.get("/{producto_id}")
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Actualizar producto (solo admin)
@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    admin_id: int,
    nombre: str,
    descripcion: str,
    precio: float,
    stock: int,
    imagen: str,
    db: Session = Depends(get_db)
):
    admin = db.query(models.Usuario).filter(models.Usuario.id == admin_id, models.Usuario.rol == "admin").first()
    if not admin:
        raise HTTPException(status_code=403, detail="No tiene permisos para actualizar productos.")

    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.nombre = nombre
    producto.descripcion = descripcion
    producto.precio = precio
    producto.stock = stock
    producto.imagen = imagen
    db.commit()
    return {"mensaje": "Producto actualizado"}

# Eliminar producto (solo admin)
@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(models.Usuario).filter(models.Usuario.id == admin_id, models.Usuario.rol == "admin").first()
    if not admin:
        raise HTTPException(status_code=403, detail="No tiene permisos para eliminar productos.")

    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto)
    db.commit()
    return {"mensaje": "Producto eliminado"}
