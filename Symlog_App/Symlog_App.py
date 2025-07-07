# Symlog_App.py

import sys
import os
import tkinter as tk
from symlog_ui import SymlogApp

def get_app_base_dir():
    """Obtiene el directorio base del lanzador principal."""
    if getattr(sys, 'frozen', False):
        # Cuando es un .exe, está en su propia subcarpeta. Hay que subir un nivel.
        return os.path.dirname(os.path.dirname(sys.executable))
    else:
        # Cuando es un script, también subimos un nivel desde su carpeta.
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SymlogApp(root)
        root.mainloop()
    except Exception as e:
        # Fallback por si la UI no se puede iniciar
        import traceback
        print("ERROR FATAL AL INICIAR LA APLICACIÓN SYMLOG")
        traceback.print_exc()
        input("Presiona Enter para salir.")