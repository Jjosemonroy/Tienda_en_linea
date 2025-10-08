#!/usr/bin/env python3
"""
Script para ejecutar la tienda en línea completa
Inicia tanto el backend como el frontend para acceso desde red local
"""

import subprocess
import threading
import time
import socket
import os
import sys

def get_local_ip():
    """Obtener la IP local de la máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def run_backend():
    """Ejecutar el servidor backend"""
    print("🚀 Iniciando servidor backend...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Servidor backend detenido")
    except Exception as e:
        print(f"❌ Error al iniciar backend: {e}")

def run_frontend():
    """Ejecutar el servidor frontend"""
    print("🎨 Iniciando servidor frontend...")
    try:
        os.chdir("tienda-front")
        subprocess.run([
            "npm", "run", "dev", "--", "--host", "0.0.0.0"
        ], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Servidor frontend detenido")
    except Exception as e:
        print(f"❌ Error al iniciar frontend: {e}")

def main():
    local_ip = get_local_ip()
    
    print("=" * 60)
    print("🛍️  TIENDA EN LÍNEA - MODO RED LOCAL")
    print("=" * 60)
    print(f"📍 IP Local: {local_ip}")
    print(f"🔗 Backend API: http://{local_ip}:8000")
    print(f"📚 API Docs: http://{local_ip}:8000/docs")
    print(f"🎨 Frontend: http://{local_ip}:5173")
    print(f"📊 Admin Panel: http://{local_ip}:5173/admin")
    print(f"🛍️  Tienda: http://{local_ip}:5173/productos")
    print()
    print("📱 PARA ACCEDER DESDE TU CELULAR:")
    print(f"   - Asegúrate de estar en la misma red WiFi")
    print(f"   - Abre en tu navegador: http://{local_ip}:5173")
    print()
    print("⏹️  Presiona Ctrl+C en cualquier terminal para detener")
    print("=" * 60)
    
    # Verificar dependencias
    print("\n🔍 Verificando dependencias...")
    
    # Verificar si existe la carpeta tienda-front
    if not os.path.exists("tienda-front"):
        print("❌ Carpeta 'tienda-front' no encontrada")
        print("   Asegúrate de estar en el directorio raíz del proyecto")
        return
    
    # Verificar si existe node_modules
    if not os.path.exists("tienda-front/node_modules"):
        print("📦 Instalando dependencias del frontend...")
        os.chdir("tienda-front")
        subprocess.run(["npm", "install"], check=True)
        os.chdir("..")
    
    print("✅ Dependencias verificadas")
    print()
    
    # Iniciar servidores en hilos separados
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)
    
    try:
        backend_thread.start()
        time.sleep(2)  # Esperar un poco para que el backend inicie
        frontend_thread.start()
        
        print("🎯 Servidores iniciados correctamente!")
        print("🌐 La aplicación está disponible en:")
        print(f"   Frontend: http://{local_ip}:5173")
        print(f"   Backend: http://{local_ip}:8000")
        
        # Mantener el script corriendo
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidores...")
        print("✅ Servidores detenidos")

if __name__ == "__main__":
    main()
