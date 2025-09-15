# support_popup.py (Versión Definitiva para PyInstaller)

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
        # Si no es un .exe, usamos la ruta normal del directorio actual.
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# --- FIN DE LA FUNCIÓN ---


def show_support_popup():
    """
    Muestra una ventana emergente modal en su propia instancia de Tkinter.
    """
    temp_root = tk.Tk()
    temp_root.withdraw()
    popup = None
    try:
        popup = tk.Toplevel(temp_root)
        popup.title("Apoya este Proyecto")
        popup.minsize(300, 350)
        
        def on_close_popup():
            if temp_root and temp_root.winfo_exists():
                temp_root.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close_popup)

        # --- ESTRUCTURA DE SCROLL ---
        main_container = ttk.Frame(popup)
        main_container.pack(expand=True, fill=tk.BOTH)
        main_container.grid_rowconfigure(0, weight=1); main_container.grid_columnconfigure(0, weight=1)
        canvas = tk.Canvas(main_container, bd=0, highlightthickness=0); canvas.grid(row=0, column=0, sticky='nsew')
        v_scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview); v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar = ttk.Scrollbar(main_container, orient="horizontal", command=canvas.xview); h_scrollbar.grid(row=1, column=0, sticky='ew')
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        scrollable_frame = ttk.Frame(canvas, padding="20"); canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # --- FIN DE ESTRUCTURA DE SCROLL ---

        # --- Contenido del Pop-up ---
        ttk.Label(scrollable_frame, text="❤️", font=("Segoe UI Emoji", 20)).pack(pady=(0, 5))
        support_text = "Si esta herramienta te es útil, considera apoyar su desarrollo futuro."
        ttk.Label(scrollable_frame, text=support_text, wraplength=350, justify=tk.CENTER).pack(pady=(0, 20))
        
        support_url = "https://www.buymeacoffee.com/Yzaak64"
        
        # --- LÍNEA CLAVE: Busca la imagen usando nuestra función especial ---
        image_path = resource_path("buy_me_a_coffee.png")
        
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img.thumbnail((217, 60), Image.Resampling.LANCZOS) 
                popup.coffee_photo = ImageTk.PhotoImage(img) 
                coffee_button = tk.Button(scrollable_frame, image=popup.coffee_photo, 
                                          command=lambda: [webbrowser.open_new(support_url), on_close_popup()], 
                                          borderwidth=0, cursor="hand2")
                coffee_button.pack(pady=10)
            else:
                raise FileNotFoundError("La imagen de apoyo no se encontró.")
        except Exception as e:
            traceback.print_exc()
            fallback_button = ttk.Button(scrollable_frame, text="☕ Buy me a coffee", 
                                         command=lambda: [webbrowser.open_new(support_url), on_close_popup()])
            fallback_button.pack(pady=10)
        
        continue_button = ttk.Button(scrollable_frame, text="Continuar al programa", command=on_close_popup)
        continue_button.pack(pady=(20, 0))

        # --- Centrar y mostrar la ventana ---
        popup.update_idletasks()
        p_width = min(scrollable_frame.winfo_reqwidth() + 40, popup.winfo_screenwidth() - 50)
        p_height = min(scrollable_frame.winfo_reqheight() + 40, popup.winfo_screenheight() - 50)
        x = (popup.winfo_screenwidth() // 2) - (p_width // 2)
        y = (popup.winfo_screenheight() // 2) - (p_height // 2)
        popup.geometry(f"{p_width}x{p_height}+{x}+{y}")
        popup.attributes('-topmost', True); popup.focus_force(); popup.grab_set()

        temp_root.mainloop()

    except Exception as e:
        print(f"\n--- ERROR CATASTRÓFICO DENTRO DE show_support_popup: {e} ---")
        traceback.print_exc()
        if temp_root and temp_root.winfo_exists():
            temp_root.destroy()