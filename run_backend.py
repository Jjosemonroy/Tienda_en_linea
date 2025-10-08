#!/usr/bin/env python3
"""
Script para ejecutar el backend de la tienda en línea
Permite acceso desde dispositivos en la misma red local
"""

import uvicorn
import os
import socket

def get_local_ip():
    """Obtener la IP local de la máquina"""
    try:
        # Conectar a un socket para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"🌐 Servidor backend iniciando...")
    print(f"📍 IP Local: {local_ip}")
    print(f"🔗 URL Backend: http://{local_ip}:8000")
    print(f"📚 API Docs: http://{local_ip}:8000/docs")
    print(f"📊 Admin Panel: http://{local_ip}:5173/admin")
    print(f"🛍️  Tienda: http://{local_ip}:5173/productos")
    print(f"\n📱 Para acceder desde tu celular:")
    print(f"   - Asegúrate de estar en la misma red WiFi")
    print(f"   - Abre en tu navegador: http://{local_ip}:5173")
    print(f"\n⏹️  Presiona Ctrl+C para detener el servidor")
    print("=" * 60)
    
    # Ejecutar el servidor
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Escuchar en todas las interfaces
        port=8000,
        reload=True,
        log_level="info"
    )
