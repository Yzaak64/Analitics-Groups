# popapp.py (Versión Definitiva para PyInstaller)

import tkinter as tk
from tkinter import ttk
import webbrowser
import sys
import os
from PIL import Image, ImageTk
import traceback

# --- FUNCIÓN CLAVE PARA ENCONTRAR ARCHIVOS DENTRO DEL .EXE ---
def resource_path(relative_path):
    """
    Obtiene la ruta absoluta al recurso. Funciona para el modo de desarrollo
    y para cuando la aplicación está empaquetada con PyInstaller.
    """
    try:
        # PyInstaller crea una carpeta temporal y guarda su ruta en _MEIPASS.
        base_path = sys._MEIPASS
    except Exception:
        # Si no es un .exe, usamos la ruta normal del directorio actual del script.
        base_path = os.path.abspath(".")

    # Unimos la ruta base con la ruta relativa del archivo que queremos.
    return os.path.join(base_path, relative_path)
# --- FIN DE LA FUNCIÓN ---


def show_coffee_popup():
    """
    Muestra una ventana emergente en su propia instancia de Tkinter,
    bloqueando la ejecución del script principal hasta que se cierre.
    """
    # Creamos una ventana raíz temporal y la ocultamos.
    temp_root = tk.Tk()
    temp_root.withdraw()

    popup = None
    try:
        popup = tk.Toplevel(temp_root)
        popup.title("Apoya este Proyecto")
        
        # --- Contenedor Principal con Scroll ---
        canvas = tk.Canvas(popup)
        v_scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(popup, orient="horizontal", command=canvas.xview)
        popup_frame = ttk.Frame(canvas, padding="20")
        
        popup_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=popup_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        
        def on_close_popup():
            temp_root.quit()
            temp_root.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close_popup)
        
        # --- Contenido del Popup ---
        ttk.Label(popup_frame, text="¡Hola!", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))
        
        support_text = "Si esta herramienta te resulta útil, considera apoyar su desarrollo futuro con un café."
        ttk.Label(popup_frame, text=support_text, wraplength=350, justify=tk.CENTER).pack(pady=(0, 20))
        
        support_url = "https://www.buymeacoffee.com/Yzaak64"
        
        # --- LÍNEA CLAVE: Obtenemos la ruta a la imagen usando nuestra función especial ---
        image_path = resource_path("Buy_Coffe.png")
        
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img.thumbnail((300, 100))
                popup.coffee_photo = ImageTk.PhotoImage(img) 
                
                coffee_button = tk.Button(popup_frame, image=popup.coffee_photo, 
                                          command=lambda: [webbrowser.open_new(support_url), on_close_popup()], 
                                          borderwidth=0, cursor="hand2")
                coffee_button.pack(pady=10)
            else:
                raise FileNotFoundError("La imagen no se encontró en la ruta esperada.")
        except Exception:
            traceback.print_exc()
            fallback_button = ttk.Button(popup_frame, text="☕ Invítame un café", 
                                         command=lambda: [webbrowser.open_new(support_url), on_close_popup()])
            fallback_button.pack(pady=10)
        
        continue_button = ttk.Button(popup_frame, text="Continuar al programa", command=on_close_popup)
        continue_button.pack(pady=(20, 0))

        # --- Lógica para centrar y mostrar la ventana ---
        popup.update_idletasks()
        p_width = max(popup_frame.winfo_reqwidth() + 40, 400); p_height = popup_frame.winfo_reqheight() + 40
        s_width = popup.winfo_screenwidth(); s_height = popup.winfo_screenheight()
        x = (s_width // 2) - (p_width // 2); y = (s_height // 2) - (p_height // 2)
        popup.geometry(f"{p_width}x{p_height}+{x}+{y}"); popup.minsize(350, 300)
        popup.attributes('-topmost', True); popup.deiconify(); popup.focus_force(); popup.grab_set()
        
        temp_root.mainloop()

    except Exception as e:
        print(f"ERROR FATAL en show_coffee_popup: {e}")
        traceback.print_exc()
        if temp_root:
            temp_root.destroy()