# AnaliticsGroups.py (Versión Definitiva para PyInstaller)

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import traceback

try:
    from PIL import Image, ImageTk
except ImportError:
    messagebox.showerror("Dependencia Crítica Faltante", "La librería 'Pillow' no está instalada.")
    sys.exit(1)

# --- FUNCIÓN MEJORADA PARA ENCONTRAR RECURSOS ---
def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si no es un .exe, _MEIPASS no existe, usamos la ruta normal
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# --- FIN DE LA FUNCIÓN ---

# Variable global para el directorio base del lanzador
# La definimos aquí para que el resto del código la use
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
active_processes = {}

def launch_app(app_name, subfolder, exe_name):
    """Lanza un ejecutable que se encuentra en una subcarpeta."""
    if app_name in active_processes and active_processes[app_name].poll() is None:
        messagebox.showinfo("Aplicación en Ejecución", 
                            f"La aplicación '{app_name}' ya se está ejecutando.\n\n"
                            "Por favor, cierre la ventana existente antes de abrir una nueva.")
        return

    # Usamos BASE_DIR para encontrar las otras aplicaciones
    path_to_exe = os.path.normpath(os.path.join(BASE_DIR, subfolder, exe_name))
    
    if not os.path.exists(path_to_exe):
        messagebox.showerror("Error de Archivo", f"No se pudo encontrar el ejecutable:\n{path_to_exe}")
        return
        
    try:
        working_dir = os.path.dirname(path_to_exe)
        process = subprocess.Popen([path_to_exe], cwd=working_dir)
        active_processes[app_name] = process
    except Exception as e:
        messagebox.showerror("Error al Lanzar", f"No se pudo iniciar la aplicación:\n{e}")

class AppLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AnaliticsGroups Suite")
        self.geometry("600x650")
        self.minsize(450, 550)

        # --- CAMBIO: Usamos resource_path para encontrar el ícono ---
        icon_path = resource_path(os.path.join("Recursos", "AnaliticsGroups.ico"))
        if os.path.exists(icon_path):
            try: self.iconbitmap(icon_path)
            except tk.TclError: print(f"ADVERTENCIA: No se pudo cargar el icono.")
        
        # ... (El resto del __init__ no cambia) ...
        self.update_idletasks(); x_pos = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2); y_pos = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2); self.geometry(f'+{x_pos}+{y_pos}')
        main_container = ttk.Frame(self); main_container.pack(fill=tk.BOTH, expand=True); main_container.grid_rowconfigure(0, weight=1); main_container.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(main_container); v_scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview); h_scrollbar = ttk.Scrollbar(main_container, orient="horizontal", command=self.canvas.xview); self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew"); v_scrollbar.grid(row=0, column=1, sticky="ns"); h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.scrollable_frame = ttk.Frame(self.canvas, padding="20"); self.frame_on_canvas = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure); self.canvas.bind("<Configure>", self._center_frame_on_canvas)
        bottom_bar = ttk.Frame(self, padding=(10, 5), style="Bottom.TFrame"); bottom_bar.pack(fill=tk.X, side='bottom')
        style = ttk.Style(self); style.configure("Bottom.TFrame", background="#f0f0f0"); style.configure("Exit.TButton", font=("Helvetica", 10, "bold")); style.configure("Title.TLabel", font=("Helvetica", 10, "bold")); style.configure("Desc.TLabel", font=("Helvetica", 9, "italic"))
        ttk.Label(self.scrollable_frame, text="AnaliticsGroups Suite", font=("Helvetica", 18, "bold")).pack(pady=(0, 20))
        self.create_image_button(parent=self.scrollable_frame, image_name="Red_Sociograma.png", title="Red Sociograma:", description="Análisis de relaciones y elecciones grupales.", command=lambda: launch_app("Red Sociograma", "Red Sociograma", "Red_Sociograma_App.exe"))
        self.create_image_button(parent=self.scrollable_frame, image_name="Hemphill.png", title="Cuestionario Hemphill:", description="Calificación del Cuestionario de Descripción de Grupos.", command=lambda: launch_app("Cuestionario Hemphill", "Hemphill", "Hemphill.exe"))
        self.create_image_button(parent=self.scrollable_frame, image_name="SYMLOG.png", title="SYMLOG:", description="Análisis de perfiles de comportamiento grupal.", command=lambda: launch_app("SYMLOG", "SYMLOG", "SYMLOG.exe"))
        ttk.Button(bottom_bar, text="Salir de la Suite", command=self.destroy, style="Exit.TButton").pack(side='right')

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _center_frame_on_canvas(self, event=None):
        canvas_width = self.canvas.winfo_width(); canvas_height = self.canvas.winfo_height()
        frame_width = self.scrollable_frame.winfo_reqwidth(); frame_height = self.scrollable_frame.winfo_reqheight()
        new_x = max(0, (canvas_width - frame_width) // 2); new_y = max(0, (canvas_height - frame_height) // 2)
        self.canvas.coords(self.frame_on_canvas, new_x, new_y)

    def create_image_button(self, parent, image_name, title, description, command):
        button_frame = ttk.Frame(parent, padding=(0, 10))
        button_frame.pack(fill=tk.X)
        
        # --- CAMBIO: Usamos resource_path para encontrar las imágenes de los botones ---
        image_path = resource_path(os.path.join("Recursos", image_name))
        
        try:
            img = Image.open(image_path)
            img.thumbnail((350, 120)) 
            photo_image = ImageTk.PhotoImage(img)
            image_button = tk.Button(button_frame, image=photo_image, command=command, borderwidth=0, highlightthickness=0, cursor="hand2")
            image_button.image = photo_image; image_button.pack()
            ttk.Label(button_frame, text=title, style="Title.TLabel").pack(pady=(5, 0))
            ttk.Label(button_frame, text=description, style="Desc.TLabel").pack(pady=(2, 0))
        except FileNotFoundError:
            print(f"ADVERTENCIA: No se encontró la imagen en la ruta: '{image_path}'. Mostrando botón de texto.")
            fallback_text = title.replace(':', ''); fallback_button = ttk.Button(button_frame, text=fallback_text, command=command); fallback_button.pack()
            ttk.Label(button_frame, text=description, style="Desc.TLabel").pack(pady=(5, 0))
        except Exception as e:
            print(f"ERROR al cargar '{image_name}': {e}")
            fallback_button = ttk.Button(button_frame, text=f"Error al cargar", state="disabled"); fallback_button.pack()

if __name__ == "__main__":
    try:
        app = AppLauncher()
        app.mainloop()
    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error Fatal", f"La aplicación ha fallado:\n\n{e}")