# ===================================================================================
# Hemphill.py (LANZADOR PRINCIPAL - VERSIÓN DE PRODUCCIÓN)
# Este es el archivo que se debe ejecutar.
# Muestra el pop-up de apoyo y luego lanza la aplicación principal.
# ===================================================================================

import tkinter as tk
import sys
import os

def get_app_base_dir():
    """Obtiene el directorio base del lanzador principal."""
    if getattr(sys, 'frozen', False):
        # Cuando es un .exe, está en su propia subcarpeta. Hay que subir un nivel.
        return os.path.dirname(os.path.dirname(sys.executable))
    else:
        # Cuando es un script, también subimos un nivel desde su carpeta.
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
# Añadir la carpeta actual al path para asegurar que los imports funcionen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Importar las funciones y clases necesarias de los otros módulos
    from app_logic import HemphillApp
except ImportError as e:
    # Si falla, es porque falta un archivo. Mostramos un error claro.
    print(f"ERROR: No se pudo importar un módulo necesario: {e}")
    print("Asegúrate de que 'app_logic.py' están en la misma carpeta que 'Hemphill.py'.")
    input("Presiona Enter para salir...")
    sys.exit(1)


if __name__ == "__main__":
    try:
        # 1. Crear e iniciar la aplicación principal directamente.
        app = HemphillApp()
        app.mainloop()
        
    except Exception as e:
        print(f"ERROR FATAL en la aplicación principal: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")