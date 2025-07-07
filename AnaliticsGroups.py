# AnaliticsGroups.py (Versión Corregida para lanzar .exe)

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import traceback
import webbrowser

try:
    from PIL import Image, ImageTk
except ImportError:
    messagebox.showerror("Dependencia Crítica Faltante", "La librería 'Pillow' no está instalada.")
    sys.exit(1)

def get_base_dir():
    """Obtiene el directorio base, funciona para script y para .exe."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()

# --- INICIO DE CAMBIOS IMPORTANTES ---
def get_base_dir():
    """Obtiene el directorio base, funciona para script y para .exe."""
    if getattr(sys, 'frozen', False):
        # Si se ejecuta como un .exe empaquetado
        return os.path.dirname(sys.executable)
    else:
        # Si se ejecuta como un script .py
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
active_processes = {}

def launch_app(app_name, subfolder, exe_name):
    """Lanza un ejecutable que se encuentra en una subcarpeta."""
    if app_name in active_processes and active_processes[app_name].poll() is None:
        messagebox.showinfo("Aplicación en Ejecución", 
                            f"La aplicación '{app_name}' ya se está ejecutando.\n\n"
                            "Por favor, cierre la ventana existente antes de abrir una nueva.")
        return

    # Construye la ruta al ejecutable
    path_to_exe = os.path.normpath(os.path.join(BASE_DIR, subfolder, exe_name))
    
    if not os.path.exists(path_to_exe):
        messagebox.showerror("Error de Archivo", f"No se pudo encontrar el ejecutable:\n{path_to_exe}")
        return
        
    try:
        print(f"INFO: Lanzando '{path_to_exe}'...")
        # Cambiamos el directorio de trabajo para que el subprograma encuentre sus propios recursos
        working_dir = os.path.dirname(path_to_exe)
        process = subprocess.Popen([path_to_exe], cwd=working_dir)
        active_processes[app_name] = process
        
    except Exception as e:
        messagebox.showerror("Error al Lanzar", f"No se pudo iniciar la aplicación:\n{e}")

class AppLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AnaliticsGroups Suite")
        self.geometry("500x800")

        icon_path = os.path.join(BASE_DIR, "Recursos", "AnaliticsGroups.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except tk.TclError:
                print(f"ADVERTENCIA: No se pudo cargar el icono desde '{icon_path}'.")
        
        # ... (el resto de la configuración de la ventana es igual) ...
        self.update_idletasks()
        x_pos = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y_pos = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f'+{x_pos}+{y_pos}')
        self.resizable(False, False)

        main_content_frame = ttk.Frame(self, padding="20")
        main_content_frame.pack(fill=tk.BOTH, expand=True)
        
        bottom_bar = ttk.Frame(self, padding=(10, 5), style="Bottom.TFrame")
        bottom_bar.pack(fill=tk.X, side='bottom')
        
        style = ttk.Style(self)
        style.configure("Bottom.TFrame", background="#f0f0f0")
        style.configure("Exit.TButton", font=("Helvetica", 10, "bold"))
        style.configure("Title.TLabel", font=("Helvetica", 10, "bold"))
        style.configure("Desc.TLabel", font=("Helvetica", 9, "italic"))

        ttk.Label(main_content_frame, text="AnaliticsGroups Suite", font=("Helvetica", 18, "bold")).pack(pady=(0, 20))

        # --- Creación de los botones con las llamadas corregidas ---
        self.create_image_button(
            parent=main_content_frame,
            image_name="Red_Sociograma.png",
            title="Red Sociograma:",
            description="Análisis de relaciones y elecciones grupales.",
            # CAMBIO: El segundo argumento ahora es el nombre de la carpeta final
            command=lambda: launch_app("Red Sociograma", "Red Sociograma", "Red Sociograma.exe")
        )
        self.create_image_button(
            parent=main_content_frame,
            image_name="Hemphill.png",
            title="Cuestionario Hemphill:",
            description="Calificación del Cuestionario de Descripción de Grupos.",
            # CAMBIO: El segundo argumento ahora es el nombre de la carpeta final
            command=lambda: launch_app("Cuestionario Hemphill", "Hemphill", "Hemphill.exe")
        )
        self.create_image_button(
            parent=main_content_frame,
            image_name="SYMLOG.png",
            title="SYMLOG:",
            description="Análisis de perfiles de comportamiento grupal.",
            # CAMBIO: El segundo argumento ahora es el nombre de la carpeta final
            command=lambda: launch_app("SYMLOG", "SYMLOG", "SYMLOG.exe")
        )
        
        ttk.Separator(main_content_frame, orient='horizontal').pack(fill='x', pady=20)

        self.create_image_button(
            parent=main_content_frame,
            image_name="Buy_Coffe.png",
            title="Apoya el Proyecto:",
            description="Si te gusta esta herramienta, ¡considera invitar un café!",
            command=self.open_support_link
        )
        
        ttk.Button(bottom_bar, text="Salir de la Suite", command=self.destroy, style="Exit.TButton").pack(side='right')

    def open_support_link(self):
        support_url = "https://www.buymeacoffee.com/Yzaak64"
        print(f"INFO: Abriendo enlace de apoyo: {support_url}")
        webbrowser.open_new_tab(support_url)

    def create_image_button(self, parent, image_name, title, description, command):
        button_frame = ttk.Frame(parent, padding=(0, 10))
        button_frame.pack(fill=tk.X)
        
        image_path = os.path.join(BASE_DIR, "Recursos", image_name)
        
        try:
            img = Image.open(image_path)
            # Redimensionar la imagen para que no sea tan grande
            img.thumbnail((350, 120)) 
            photo_image = ImageTk.PhotoImage(img)
            
            image_button = tk.Button(
                button_frame, image=photo_image, command=command,
                borderwidth=0, highlightthickness=0, cursor="hand2"
            )
            image_button.image = photo_image
            image_button.pack()
            
            ttk.Label(button_frame, text=title, style="Title.TLabel").pack(pady=(5, 0))
            ttk.Label(button_frame, text=description, style="Desc.TLabel").pack(pady=(2, 0))

        except FileNotFoundError:
            print(f"ADVERTENCIA: No se encontró la imagen '{image_name}'.")
            fallback_text = title.replace(':', '')
            fallback_button = ttk.Button(button_frame, text=fallback_text, command=command)
            fallback_button.pack()
            ttk.Label(button_frame, text=description, style="Desc.TLabel").pack(pady=(5, 0))
        except Exception as e:
            print(f"ERROR al cargar '{image_name}': {e}")
            fallback_button = ttk.Button(button_frame, text=f"Error al cargar", state="disabled")
            fallback_button.pack()

if __name__ == "__main__":
    try:
        app = AppLauncher()
        app.mainloop()
    except Exception as e:
        print("\n" + "="*60 + "\n  ERROR FATAL\n" + "="*60)
        traceback.print_exc()
        input("La aplicación ha fallado. Presiona Enter para salir...")