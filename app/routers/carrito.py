# app/routers/carrito.py

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from .. import database, models
from datetime import datetime
from pydantic import BaseModel, conint

router = APIRouter(prefix="/carrito", tags=["Carrito"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo para agregar/eliminar producto del carrito
class CarritoItemRequest(BaseModel):
    usuario_id: conint(gt=0)
    producto_id: conint(gt=0)
    cantidad: conint(gt=0) = 1

# 1. Agregar producto al carrito
@router.post("/agregar")
def agregar_al_carrito(request: CarritoItemRequest = Body(...), db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == request.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    existente = db.query(models.Carrito).filter(
        models.Carrito.usuario_id == request.usuario_id,
        models.Carrito.producto_id == request.producto_id
    ).first()

    if existente:
        existente.cantidad += request.cantidad
    else:
        nuevo_item = models.Carrito(usuario_id=request.usuario_id, producto_id=request.producto_id, cantidad=request.cantidad)
        db.add(nuevo_item)

    db.commit()
    return {"mensaje": "Producto agregado al carrito"}

# 2. Ver contenido del carrito por usuario
@router.get("/{usuario_id}")
def ver_carrito(usuario_id: int, db: Session = Depends(get_db)):
    items = (
        db.query(
            models.Carrito.id,
            models.Producto.nombre.label("producto"),
            models.Producto.precio,
            models.Carrito.cantidad,
            (models.Producto.precio * models.Carrito.cantidad).label("total_linea")
        )
        .join(models.Producto, models.Carrito.producto_id == models.Producto.id)
        .filter(models.Carrito.usuario_id == usuario_id)
        .all()
    )

    resultado = []
    total_general = 0

    for item in items:
        total_linea = float(item.total_linea)
        resultado.append({
            "id": item.id,
            "producto": item.producto,
            "precio": float(item.precio),
            "cantidad": item.cantidad,
            "total_linea": item.total_linea
        })
        total_general += total_linea

    return {
        "usuario_id": usuario_id,
        "items": resultado,
        "total_carrito": round(total_general, 2)
    }


# 3. Eliminar un producto específico del carrito
@router.delete("/eliminar")
def eliminar_item(request: CarritoItemRequest = Body(...), db: Session = Depends(get_db)):
    item = db.query(models.Carrito).filter(
        models.Carrito.usuario_id == request.usuario_id,
        models.Carrito.producto_id == request.producto_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="El producto no está en el carrito")

    db.delete(item)
    db.commit()
    return {"mensaje": "Producto eliminado del carrito"}

# 4. Vaciar todo el carrito del usuario
@router.delete("/vaciar/{usuario_id}")
def vaciar_carrito(usuario_id: int, db: Session = Depends(get_db)):
    db.query(models.Carrito).filter(models.Carrito.usuario_id == usuario_id).delete()
    db.commit()
    return {"mensaje": "Carrito vaciado"}

# 5.finalizar la compra
from datetime import datetime

@router.post("/finalizar/{usuario_id}")
def finalizar_compra(usuario_id: int, db: Session = Depends(get_db)):
    # Obtener contenido del carrito
    items = (
        db.query(
            models.Carrito.producto_id,
            models.Carrito.cantidad,
            models.Producto.precio
        )
        .join(models.Producto, models.Carrito.producto_id == models.Producto.id)
        .filter(models.Carrito.usuario_id == usuario_id)
        .all()
    )

    if not items:
        raise HTTPException(status_code=400, detail="El carrito está vacío.")

    # Calcular total
    total = sum(float(item.precio) * item.cantidad for item in items)

    # Crear la venta
    venta = models.Venta(
        usuario_id=usuario_id,
        fecha=datetime.now(),
        total=total
    )
    db.add(venta)
    db.commit()
    db.refresh(venta)

    # Crear detalle_venta y descontar stock
    for item in items:
        detalle = models.DetalleVenta(
            venta_id=venta.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=item.precio
        )
        db.add(detalle)

        producto = db.query(models.Producto).filter(models.Producto.id == item.producto_id).first()
        if producto.stock < item.cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para el producto ID {item.producto_id}")
        producto.stock -= item.cantidad

    # Vaciar el carrito
    db.query(models.Carrito).filter(models.Carrito.usuario_id == usuario_id).delete()

    db.commit()

    return {
        "mensaje": "Compra finalizada exitosamente",
        "venta_id": venta.id,
        "total_pagado": round(total, 2)
    }
