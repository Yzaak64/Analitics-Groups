# Hemphill_App.py (Lanzador Principal - Versión Definitiva)

import sys
import os
import traceback

# Añadir la carpeta actual al path para asegurar que los módulos locales se encuentren.
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

try:
    # Importar las funciones y clases necesarias de tus otros archivos.
    from popapp import show_coffee_popup
    from app_logic import HemphillApp
except ImportError as e:
    # Si falta un archivo .py, muestra un error claro y sale.
    print(f"ERROR: No se pudo importar un módulo necesario: {e}")
    # En un .exe, este input no se verá, pero es útil para depurar.
    input("Presiona Enter para salir...")
    sys.exit(1)


if __name__ == "__main__":
    try:
        # 1. Mostrar el pop-up de apoyo primero.
        #    Esta función detiene la ejecución del programa hasta que el usuario
        #    cierra el popup.
        print("Mostrando pop-up de apoyo...")
        show_coffee_popup()
        print("Pop-up cerrado. Iniciando aplicación principal...")

        # 2. Una vez que el popup se ha cerrado, crear e iniciar la
        #    aplicación principal desde app_logic.py.
        app = HemphillApp()
        app.mainloop()
        
    except Exception as e:
        # Captura cualquier error fatal que no haya sido manejado dentro de la app.
        print(f"ERROR FATAL en la aplicación principal: {e}")
        traceback.print_exc()
        input("Presiona Enter para salir...")