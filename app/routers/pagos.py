from turtle import mode
from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app import database, models
from app.schemas import (
    MetodoPagoCreate,
    MetodoPagoResponse,
    EstadoTransaccionCreate,
    EstadoTransaccionResponse,
    TransaccionCreate,
    TransaccionResponse,
    DireccionEnvioCreate,
    DireccionEnvioResponse,
    DireccionEnvioResponse,
    ProcesoPagoRequest
)
from app.auth import get_current_user
from datetime import datetime
import uuid

router = APIRouter(prefix="/pagos", tags=["Pagos"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#obtener metodos de pago disponibles
@router.get("/metodos-pago")
def obtener_metodos_pago(db: Session = Depends(get_db)):
    metodos = db.query(models.MetodoPago).filter(models.MetodoPago.activo == True).all()
    return metodos

# obtener direcciones de envio disponibles
@router.get("/direcciones/{usuario_id}")
def obtener_direcciones_envio(usuario_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    direcciones = db.query(models.DireccionEnvio).filter(models.DireccionEnvio.usuario_id == usuario_id == user.id).all()
    return direcciones

#crear nueva direccion de envio
@router.post("/direcciones")
def crear_direccion_envio(direccion: DireccionEnvioCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):

    usuario_id = user["id"]

    if direccion.es_principal:
        db.query(models.DireccionEnvio).filter(models.DireccionEnvio.usuario_id == usuario_id).update({"es_principal": False})

    nueva_direccion = models.DireccionEnvio(
        usuario_id=usuario_id,
        alias=direccion.alias,
        nombre_completo=direccion.nombre_completo,
        direccion=direccion.direccion,
        ciudad=direccion.ciudad,
        codigo_postal=direccion.codigo_postal,
        telefono=direccion.telefono,
        es_principal=direccion.es_principal,
        fecha_creacion=datetime.now()
    )

    db.add(nueva_direccion)
    db.commit()
    db.refresh(nueva_direccion)

    return {"mensaje": "Direccion de envio creada exitosamente", "direccion": nueva_direccion.id}

#procesar pago
@router.post("/procesar")
def procesar_pago(request: ProcesoPagoRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    #verificar que la venta existe
    venta = db.query(models.Venta).filter(models.Venta.id == request.venta_id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    #verificar que el metodo de pago existe
    metodo_pago = db.query(models.MetodoPago).filter(models.MetodoPago.id == request.metodo_pago_id).first()
    if not metodo_pago:
        raise HTTPException(status_code=404, detail="Metodo de pago no encontrado")

    #obtener estado "pendiente" (asumiendo que existe)
    estado_pendiente = db.query(models.EstadoTransaccion).filter(models.EstadoTransaccion.nombre == "pendiente").first()
    if not estado_pendiente:
        #crear estado "pendiente" si no existe
        estado_pendiente = models.EstadoTransaccion(nombre="pendiente", descripcion="Transaccion de procesamiento")
        db.add(estado_pendiente)
        db.commit()
        db.refresh(estado_pendiente)

#generar referencia de transaccion
    referencia = f"TXN_{datetime.now().strftime('%Y%m%d')}_{str(uuid.uuid4())[:8].upper()}"

    #crear transaccion
    transaccion = models.Transaccion(
        venta_id=request.venta_id,
        metodo_pago_id=request.metodo_pago_id,
        estado_id=estado_pendiente.id,
        referencia=referencia,
        monto=venta.total,
        datos_pago=request.datos_pago,
        fecha_creacion=datetime.now()
    )

    db.add(transaccion)
    db.commit()
    db.refresh(transaccion)

    #aqui ira la logica real de procesamiento del pago
    estado_aprobado = db.query(models.EstadoTransaccion).filter(models.EstadoTransaccion.nombre == "aprobado").first()
    if not estado_aprobado:
        estado_aprobado = models.EstadoTransaccion(nombre="aprobado", descripcion="Transaccion aprobada")
        db.add(estado_aprobado)
        db.commit()
        db.refresh(estado_aprobado)

        #actualizar estado de la transaccion
        transaccion.estado_id = estado_aprobado.id
        transaccion.fecha_actualizacion = datetime.now()
        db.commit()

        return {
            "mensaje": "Pago procesado exitosamente",
            "transaccion_id": transaccion.id,
            "referencia": referencia,
            "estado": "aprobado"
        }

#obtener historial de transacciones del usuario
@router.get("/historial/{usuario_id}")
def obtener_historial_transacciones(usuario_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    transacciones = (
        db.query(
        models.Transaccion,
        models.Venta,
        models.MetodoPago,
        models.EstadoTransaccion
    )
    .join(models.Venta, models.Transaccion.venta_id == models.Venta.id)
    .join(models.MetodoPago, models.Transaccion.metodo_pago_id == models.MetodoPago.id)
    .join(models.EstadoTransaccion, models.Transaccion.estado_id == models.EstadoTransaccion.id)
    .filter(models.Venta.usuario_id == usuario_id)
    .order_by(models.Transaccion.fecha_creacion.desc())
    .all()
    )

    resultados = []
    for txn, venta, metodo, estado in transacciones:
        resultados.append({
            "id": txn.id,
            "referencia": txn.referencia,
            "monto": float(txn.monto),
            "metodo_pago": metodo.nombre,
            "estado": estado.nombre,
            "fecha": txn.fecha_creacion,
            "total": venta.id
        })

    return resultados

@router.get("/historial-completo/{usuario_id}")
def obtener_historial_completo(usuario_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    #verificar que el usuario solo pueda ver su propio historial
    if user["id"] != usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver este historial")

    ventas = db.query(models.Venta).filter(models.Venta.usuario_id == usuario_id).order_by(models.Venta.fecha.desc()).all()

    historial_completo = []

    for venta in ventas:
        #obtener detalles de la venta
        detalles = (
            db.query(
                models.Producto.nombre.label("producto"),
                models.Producto.imagen,
                models.DetalleVenta.cantidad,
                models.DetalleVenta.precio_unitario,
                (models.DetalleVenta.cantidad * models.DetalleVenta.precio_unitario).label("subtotal")
            )
            .join(models.Producto, models.Producto.id == models.DetalleVenta.producto_id)
            .filter(models.DetalleVenta.venta_id == venta.id)
            .all()
        )

        # obtener transaccion asociada
        transaccion = (
            db.query(
                models.Transaccion,
                models.MetodoPago.nombre.label("metodo_pago"),
                models.EstadoTransaccion.nombre.label("estado_transaccion")
            )
            .join(models.MetodoPago, models.Transaccion.metodo_pago_id == models.MetodoPago.id)
            .join(models.EstadoTransaccion, models.Transaccion.estado_id == models.EstadoTransaccion.id)
            .filter(models.Transaccion.venta_id == venta.id)
            .first()
        )

        # formatear detalles de la venta
        productos = []
        for detalle in detalles:
            productos.append({
                "nombre": detalle.producto,
                "imagen": detalle.imagen,
                "cantidad": detalle.cantidad,
                "precio_unitario": float(detalle.precio_unitario),
                "subtotal": float(detalle.subtotal)
            })

        # agregar informacion de la transaccion
        venta_info = {
            "venta_id": venta.id,
            "fecha": venta.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "total": float(venta.total),
            "productos": productos,
            "transaccion": None
        }

        if transaccion:
            venta_info["transaccion"] = {
                "referencia": transaccion.Transaccion.referencia,
                "metodo_pago": transaccion.metodo_pago,
                "estado": transaccion.estado_transaccion,
                "fecha_pago": transaccion.Transaccion.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
            }

        historial_completo.append(venta_info)

    return {
        "usuario_id": usuario_id,
        "total_compras": len(historial_completo),
        "historial": historial_completo
    }