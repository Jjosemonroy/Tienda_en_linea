from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Categoria
from app.schemas import CategoriaCreate, CategoriaResponse

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.get("/", response_model=List[CategoriaResponse])
def obtener_categorias(db: Session = Depends(get_db)):
    """Obtener todas las categorías activas"""
    categorias = db.query(Categoria).filter(Categoria.activo == True).all()
    return categorias

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """Obtener una categoría específica"""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    return categoria

@router.post("/", response_model=CategoriaResponse)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """Crear una nueva categoría"""
    # Verificar si ya existe una categoría con ese nombre
    categoria_existente = db.query(Categoria).filter(Categoria.nombre == categoria.nombre).first()
    if categoria_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una categoría con ese nombre"
        )
    
    nueva_categoria = Categoria(**categoria.dict())
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

@router.put("/{categoria_id}", response_model=CategoriaResponse)
def actualizar_categoria(categoria_id: int, categoria: CategoriaCreate, db: Session = Depends(get_db)):
    """Actualizar una categoría existente"""
    categoria_db = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Verificar si el nuevo nombre ya existe en otra categoría
    categoria_existente = db.query(Categoria).filter(
        Categoria.nombre == categoria.nombre,
        Categoria.id != categoria_id
    ).first()
    if categoria_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una categoría con ese nombre"
        )
    
    for key, value in categoria.dict().items():
        setattr(categoria_db, key, value)
    
    db.commit()
    db.refresh(categoria_db)
    return categoria_db

@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """Eliminar una categoría (marcar como inactiva)"""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Marcar como inactiva en lugar de eliminar físicamente
    categoria.activo = False
    db.commit()
    
    return {"mensaje": "Categoría eliminada exitosamente"} 