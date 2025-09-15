# Symlog_App.py

import tkinter as tk
from symlog_ui import SymlogApp
from support_popup import show_support_popup
import traceback

if __name__ == "__main__":
    print("[LOG] Iniciando la aplicación.")
    
    # 1. Llamar a la función del popup PRIMERO.
    #    Esta función ahora maneja su propio bucle de Tkinter y lo bloquea todo.
    print("\n[LOG] >>> Llamando a show_support_popup...")
    show_support_popup()
    print("[LOG] <<< Retorno de show_support_popup. Continuando con la aplicación principal.\n")

    # 2. Solo DESPUÉS de que el popup se haya cerrado, creamos la aplicación principal.
    root = None
    try:
        print("[LOG] Creando la ventana raíz de la aplicación principal.")
        root = tk.Tk()
        
        print("[LOG] Creando la instancia de SymlogApp.")
        app = SymlogApp(root)
        
        print("[LOG] Iniciando el bucle principal de la aplicación (mainloop).")
        root.mainloop()
        print("[LOG] El bucle principal ha finalizado. La aplicación se está cerrando.")
        
    except Exception as e:
        print("\n--- ERROR FATAL AL INICIAR LA APLICACIÓN SYMLOG ---")
        traceback.print_exc()
        if root and root.winfo_exists():
             root.destroy()
        input("Presiona Enter para salir.")