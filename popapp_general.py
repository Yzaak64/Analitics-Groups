# popapp_general.py (Versión de Depuración Final)

import tkinter as tk
from tkinter import ttk
import webbrowser
import os
import sys

# Función para obtener la ruta base de forma segura
def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

# Intenta importar Pillow
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def show_support_popup(parent):
    popup = tk.Toplevel(parent)
    popup.title("Apoya este Proyecto")
    
    # --- Configuración de la ventana (sin cambios) ---
    popup.update_idletasks()
    p_width, p_height = 400, 220
    s_width, s_height = popup.winfo_screenwidth(), popup.winfo_screenheight()
    x, y = (s_width // 2) - (p_width // 2), (s_height // 2) - (p_height // 2)
    popup.geometry(f"{p_width}x{p_height}+{x}+{y}")
    popup.resizable(False, False)

    popup_frame = ttk.Frame(popup, padding="20")
    popup_frame.pack(expand=True, fill=tk.BOTH)
    
    ttk.Label(popup_frame, text="¡Gracias por usar esta suite!", font=("Helvetica", 14, "bold")).pack(pady=(0, 10))
    support_text = "Si estas herramientas te resultan útiles, considera apoyar su desarrollo futuro con un café."
    ttk.Label(popup_frame, text=support_text, wraplength=350, justify=tk.CENTER).pack(pady=(0, 20))

    support_url = "https://www.buymeacoffee.com/Yzaak64"
    
    # --- Construcción de la ruta y depuración ---
    base_dir = get_base_path()
    image_path = os.path.join(base_dir, "Buy_Coffe.png")

    print("--- INICIO DEPURACIÓN POP-UP ---")
    print(f"[1] ¿Pillow disponible?: {PIL_AVAILABLE}")
    print(f"[2] Ruta de imagen calculada: {image_path}")
    print(f"[3] ¿Existe el archivo en esa ruta?: {os.path.exists(image_path)}")
    print("---------------------------------")
    
    def open_link_and_close():
        webbrowser.open_new(support_url)
        popup.destroy()

    try:
        if PIL_AVAILABLE and os.path.exists(image_path):
            img = Image.open(image_path)
            img.thumbnail((200, 70))
            popup.coffee_photo = ImageTk.PhotoImage(img)
            
            coffee_button = tk.Button(popup_frame, image=popup.coffee_photo, command=open_link_and_close, borderwidth=0, cursor="hand2")
            coffee_button.pack(pady=5)
        else:
            raise RuntimeError("Fallback activado. Causa: Pillow no disponible o archivo no encontrado.")
            
    except Exception as e:
        print(f"INFO (popapp): Se activó el botón de texto. Razón: {e}")
        fallback_button = ttk.Button(popup_frame, text="☕ Invítame un café", command=open_link_and_close)
        fallback_button.pack(pady=10)
    
    continue_button = ttk.Button(popup_frame, text="Continuar al programa", command=popup.destroy)
    continue_button.pack(pady=(15, 0))

    popup.transient(parent)
    popup.grab_set()
    parent.wait_window(popup)