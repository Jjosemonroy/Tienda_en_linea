# app/routers/ventas.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from .. import database, models

router = APIRouter(prefix="/ventas", tags=["Ventas"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def historial_ventas(
    admin_id: int,
    usuario_id: Optional[int] = None,
    fecha: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    # Validar que quien consulta sea admin
    admin = db.query(models.Usuario).filter(models.Usuario.id == admin_id, models.Usuario.rol == "admin").first()
    if not admin:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden ver el historial de ventas.")

    # Obtener ventas con filtros opcionales
    query = db.query(models.Venta)
    if usuario_id:
        query = query.filter(models.Venta.usuario_id == usuario_id)
    if fecha:
        query = query.filter(models.Venta.fecha.cast(date) == fecha)

    ventas = query.all()

    historial = []

    for venta in ventas:
        detalles = (
            db.query(
                models.Producto.nombre.label("producto"),
                models.DetalleVenta.cantidad,
                models.DetalleVenta.precio_unitario,
                (models.DetalleVenta.cantidad * models.DetalleVenta.precio_unitario).label("subtotal")
            )
            .join(models.Producto, models.Producto.id == models.DetalleVenta.producto_id)
            .filter(models.DetalleVenta.venta_id == venta.id)
            .all()
        )

        detalles_format = []
        for d in detalles:
            detalles_format.append({
                "producto": d.producto,
                "cantidad": d.cantidad,
                "precio_unitario": float(d.precio_unitario),
                "subtotal": float(d.subtotal)
            })

        historial.append({
            "venta_id": venta.id,
            "usuario_id": venta.usuario_id,
            "fecha": venta.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "total": float(venta.total),
            "detalles": detalles_format
        })

    return historial

@router.get("/cliente/{usuario_id}")
def historial_cliente(usuario_id: int, db: Session = Depends(get_db)):
    ventas = db.query(models.Venta).filter(models.Venta.usuario_id == usuario_id).all()

    historial = []

    for venta in ventas:
        detalles = (
            db.query(
                models.Producto.nombre.label("producto"),
                models.DetalleVenta.cantidad,
                models.DetalleVenta.precio_unitario,
                (models.DetalleVenta.cantidad * models.DetalleVenta.precio_unitario).label("subtotal")
            )
            .join(models.Producto, models.Producto.id == models.DetalleVenta.producto_id)
            .filter(models.DetalleVenta.venta_id == venta.id)
            .all()
        )

        detalles_format = []
        for d in detalles:
            detalles_format.append({
                "producto": d.producto,
                "cantidad": d.cantidad,
                "precio_unitario": float(d.precio_unitario),
                "subtotal": float(d.subtotal)
            })

        historial.append({
            "venta_id": venta.id,
            "fecha": venta.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "total": float(venta.total),
            "detalles": detalles_format
        })

    return historial
