# symlog_ui.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import pandas as pd
import os
import sys
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
import traceback
import datetime
import webbrowser

# Importaciones desde los nuevos módulos locales
from symlog_data import all_scales_data, PLOT_SIZE_DIVISOR
from symlog_logic import calculate_from_manual_scores, calculate_from_excel, calculate_marker_size
from manual_generator_symlog import create_symlog_manual_pdf

class SymlogApp:
    def __init__(self, master):
        self.master = master
        master.title("Interfaz SYMLOG Tkinter v2.0.0")
        master.geometry("800x650")

        # --- Variables de Estado ---
        self.current_action = tk.StringVar(master)
        self.selected_scale_name = tk.StringVar(master)
        self.selected_excel_file = tk.StringVar(master)
        self.selected_json_file_plot = tk.StringVar(master)
        self.results_filename = tk.StringVar(master, value="resultados_symlog.json")
        self.results_by_scale = {}
        self.manual_item_widgets = {}
        self.manual_entry_order = []

        # --- Estilo y Layout Principal ---
        style = ttk.Style()
        style.theme_use('clam')
        
        main_frame = ttk.Frame(master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5, side=tk.TOP)
        
        ttk.Label(top_frame, text="Acción:").pack(side=tk.LEFT, padx=5)
        action_options=['Por favor, selecciona...','1. Generar Plantilla Excel','2. Ingresar Datos Manualmente','3. Procesar Archivo Excel Subido','4. Generar Gráfico desde JSON']
        self.action_combo=ttk.Combobox(top_frame, textvariable=self.current_action, values=action_options, state='readonly', width=30)
        self.action_combo.pack(side=tk.LEFT, padx=5)
        self.action_combo.current(0)
        self.action_combo.bind('<<ComboboxSelected>>', self._on_action_change)
        
        ttk.Label(top_frame, text="Escala SYMLOG:").pack(side=tk.LEFT, padx=5)
        scale_options = list(all_scales_data.keys())
        self.scale_combo=ttk.Combobox(top_frame, textvariable=self.selected_scale_name, values=scale_options, state='disabled', width=15)
        self.scale_combo.pack(side=tk.LEFT, padx=5)
        self.scale_combo.bind('<<ComboboxSelected>>', self._on_scale_change)
        
        self.action_panel_container = ttk.Frame(main_frame)
        self.action_panel_container.pack(fill=tk.BOTH, expand=True, pady=5, side=tk.TOP, after=top_frame)
        
        self.action_panels={}
        self.action_panels['1. Generar Plantilla Excel'] = self._create_template_panel(self.action_panel_container)
        self.action_panels['2. Ingresar Datos Manualmente'] = self._create_manual_panel(self.action_panel_container)
        self.action_panels['3. Procesar Archivo Excel Subido'] = self._create_excel_panel(self.action_panel_container)
        self.action_panels['4. Generar Gráfico desde JSON'] = self._create_json_plot_panel(self.action_panel_container)
        
        output_frame_container = ttk.LabelFrame(main_frame, text="Salida y Mensajes")
        output_frame_container.pack(fill=tk.X, pady=5, side=tk.BOTTOM, expand=False)
        self.output_text = scrolledtext.ScrolledText(output_frame_container, wrap=tk.WORD, height=10, state='disabled')
        self.output_text.pack(fill=tk.BOTH, expand=True)

        bottom_actions_frame = ttk.Frame(main_frame)
        bottom_actions_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))

        self.manual_button = ttk.Button(bottom_actions_frame, text="📖 Ver Manual de Usuario", command=self._open_manual)
        self.manual_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.results_widgets_container = ttk.Frame(bottom_actions_frame)
        self.results_widgets_container.pack(side=tk.RIGHT)

        style.configure('Danger.TButton', foreground='white', background='red')
        self.clear_button = ttk.Button(self.results_widgets_container, text="Limpiar Resultados", command=self._clear_all, style='Danger.TButton')
        self.clear_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.save_button = ttk.Button(self.results_widgets_container, text="Guardar Resultados", command=self._save_results)
        self.save_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.results_entry = ttk.Entry(self.results_widgets_container, textvariable=self.results_filename, width=30)
        self.results_entry.pack(side=tk.RIGHT, padx=5, pady=5)
        
        ttk.Label(self.results_widgets_container, text="Guardar como:").pack(side=tk.RIGHT, pady=5)

        self._update_action_panels()
        self._update_widget_states()
        self._log("Interfaz SYMLOG iniciada.")

    # --- Crear Paneles ---
    def _create_template_panel(self, parent):
        frame=ttk.Frame(parent,padding="10")
        ttk.Label(frame,text="Selecciona una escala y haz clic para generar una plantilla de Excel (.xlsx).").pack(pady=5,anchor="w")
        ttk.Button(frame,text="Generar y Guardar Plantilla",command=self._generate_template).pack(pady=10)
        return frame

    def _create_manual_panel(self, parent):
        frame=ttk.Frame(parent,padding="10")
        nf=ttk.Frame(frame)
        nf.pack(fill=tk.X, pady=5)
        ttk.Label(nf,text="Nombre del Participante:").pack(side=tk.LEFT,padx=5)
        self.manual_participant_name_entry=ttk.Entry(nf,width=40)
        self.manual_participant_name_entry.pack(side=tk.LEFT,padx=5,fill=tk.X,expand=True)
        icf=ttk.LabelFrame(frame,text="Puntuaciones (0-4)")
        icf.pack(fill=tk.BOTH,expand=True, pady=5)
        self.mic=tk.Canvas(icf,bd=0,highlightthickness=0,bg="#ffffff")
        self.mif=ttk.Frame(self.mic,padding="5")
        vsb=ttk.Scrollbar(icf,orient="vertical",command=self.mic.yview)
        self.mic.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right",fill="y")
        self.mic.pack(side="left",fill="both",expand=True)
        self.micw=self.mic.create_window((0,0),window=self.mif,anchor="nw",tags="self.mif")
        self.mif.bind("<Configure>", self._on_manual_items_frame_configure)
        self.mic.bind_all("<MouseWheel>", self._on_mousewheel, add='+')
        self.mic.bind_all("<Button-4>", self._on_mousewheel, add='+')
        self.mic.bind_all("<Button-5>", self._on_mousewheel, add='+')
        self.manual_add_button=ttk.Button(frame,text="Calcular y Añadir Participante",command=self._add_manual,state='disabled')
        self.manual_add_button.pack(pady=10)
        return frame

    def _create_excel_panel(self, parent):
        frame=ttk.Frame(parent,padding="10")
        ttk.Label(frame,text="Selecciona la escala, elige el archivo Excel y haz clic en procesar.").pack(pady=5,anchor="w")
        ttk.Label(frame,text="Nota: El cálculo se basa en el ORDEN de las filas. Usa la plantilla generada.").pack(pady=2,anchor="w")
        fsf=ttk.Frame(frame)
        fsf.pack(fill=tk.X,pady=5)
        ttk.Button(fsf,text="Seleccionar Archivo Excel",command=self._select_excel).pack(side=tk.LEFT,padx=5)
        self.excel_file_label=ttk.Label(fsf,text="Ningún archivo seleccionado",foreground="grey",width=40,anchor='w')
        self.excel_file_label.pack(side=tk.LEFT,padx=5,fill=tk.X,expand=True)
        self.excel_process_button=ttk.Button(frame,text="Procesar Archivo Excel",command=self._process_excel,state='disabled')
        self.excel_process_button.pack(pady=10)
        return frame

    def _create_json_plot_panel(self, parent):
        frame=ttk.Frame(parent,padding="10")
        ttk.Label(frame,text="Selecciona un archivo JSON de resultados y haz clic para generar y guardar el gráfico.").pack(pady=5,anchor="w")
        fsf=ttk.Frame(frame)
        fsf.pack(fill=tk.X,pady=5)
        ttk.Button(fsf,text="Seleccionar Archivo JSON",command=self._select_json_plot).pack(side=tk.LEFT,padx=5)
        self.json_plot_file_label=ttk.Label(fsf,text="Ningún archivo seleccionado",foreground="grey",width=40,anchor='w')
        self.json_plot_file_label.pack(side=tk.LEFT,padx=5,fill=tk.X,expand=True)
        self.json_plot_button=ttk.Button(frame,text="Generar y Guardar Gráfico",command=self._generate_and_save_plot,state='disabled')
        self.json_plot_button.pack(pady=10)
        return frame

    # --- Ayuda y Lógica UI ---
    def _log(self, msg):
        now=datetime.datetime.now().strftime("%H:%M:%S")
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END,f"[{now}] {msg}\n")
        self.output_text.config(state='disabled')
        self.output_text.see(tk.END)

    def _clear_log(self):
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.config(state='disabled')

    def _update_action_panels(self):
        sel=self.current_action.get()
        for pan in self.action_panels.values():
            if isinstance(pan, tk.Widget) and pan.winfo_ismapped():
                pan.pack_forget()
        if sel in self.action_panels:
             panel = self.action_panels[sel]
             if isinstance(panel, tk.Widget):
                 panel.pack(in_=self.action_panel_container,fill=tk.BOTH,expand=True,pady=5)
        
        if self._has_any_results():
            if not self.results_widgets_container.winfo_ismapped():
                self.results_widgets_container.pack(side=tk.RIGHT)
        else:
            if self.results_widgets_container.winfo_ismapped():
                self.results_widgets_container.pack_forget()

    def _update_widget_states(self):
        act=self.current_action.get()
        sc=self.selected_scale_name.get()
        hs=bool(sc)
        hx=bool(self.selected_excel_file.get())
        hj=bool(self.selected_json_file_plot.get())
        hr=self._has_any_results()
        
        is_data_act = act in ['1. Generar Plantilla Excel','2. Ingresar Datos Manualmente','3. Procesar Archivo Excel Subido']
        self.scale_combo.config(state='readonly' if is_data_act else 'disabled')
        
        if is_data_act and not hs and self.scale_combo.cget('values'):
            self.selected_scale_name.set(self.scale_combo['values'][0])
            hs = True
            
        if hasattr(self,'manual_add_button'):
            self.manual_add_button.config(state='normal' if act=='2. Ingresar Datos Manualmente' and hs else 'disabled')
        if hasattr(self,'excel_process_button'):
            self.excel_process_button.config(state='normal' if act=='3. Procesar Archivo Excel Subido' and hs and hx else 'disabled')
        if hasattr(self,'json_plot_button'):
            self.json_plot_button.config(state='normal' if act=='4. Generar Gráfico desde JSON' and hj else 'disabled')
        
        self.save_button.config(state='normal' if hr else 'disabled')
        self.clear_button.config(state='normal' if hr else 'disabled')
        
    def _on_action_change(self, event=None):
        self._clear_log()
        act = self.current_action.get()
        scale_auto_set = False
        previous_scale = self.selected_scale_name.get()

        if act == 'Por favor, selecciona...':
            self._log("Selecciona una acción del menú superior.")
            self.scale_combo.config(state='disabled')
            self.selected_scale_name.set("")
        else:
            self._log(f"Acción seleccionada: {act}")
            is_data_act = act in ['1. Generar Plantilla Excel', '2. Ingresar Datos Manualmente', '3. Procesar Archivo Excel Subido']
            if is_data_act:
                self.scale_combo.config(state='readonly')
                if not previous_scale and self.scale_combo.cget('values'):
                    self.selected_scale_name.set(self.scale_combo['values'][0])
                    scale_auto_set = True
            else:
                self.scale_combo.config(state='disabled')
                self.selected_scale_name.set("")

        self._update_action_panels()
        self.action_panel_container.update_idletasks()

        self.selected_excel_file.set("")
        if hasattr(self, 'excel_file_label'):
            self.excel_file_label.config(text="Ningún archivo seleccionado", foreground="grey")
        self.selected_json_file_plot.set("")
        if hasattr(self, 'json_plot_file_label'):
            self.json_plot_file_label.config(text="Ningún archivo seleccionado", foreground="grey")

        if act == '2. Ingresar Datos Manualmente':
            if self.selected_scale_name.get():
                self._update_manual_input_items()

        self._update_widget_states()

        if scale_auto_set and act != '2. Ingresar Datos Manualmente':
             self._on_scale_change()

    def _on_scale_change(self, event=None):
        sc=self.selected_scale_name.get()
        if not sc: return
        self._log(f"Escala seleccionada: {sc}")
        act=self.current_action.get()
        if act=='2. Ingresar Datos Manualmente':
            self._update_manual_input_items()
        self._update_widget_states()

    def _on_manual_items_frame_configure(self, event):
        bbox = self.mic.bbox("all")
        if bbox: self.mic.configure(scrollregion=bbox)
        self.mic.itemconfig(self.micw, width=event.width)

    def _on_mousewheel(self, event):
        widget = self.master.winfo_containing(event.x_root, event.y_root)
        is_over = False
        curr = widget
        while curr is not None:
            if curr == self.mic:
                is_over = True
                break
            curr = curr.master
        if not is_over: return
        
        if sys.platform == "win32" or sys.platform == "darwin":
            delta = -1 * int(event.delta / (120 if sys.platform == "win32" else 1))
        else: # Linux
            if event.num == 4: delta = -1
            elif event.num == 5: delta = 1
            else: delta = 0
        self.mic.yview_scroll(delta, "units")

    # --- Lógica de Acciones ---
    def _open_manual(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(base_dir, "manual_symlog.pdf")
        try:
            if not os.path.exists(pdf_path):
                self._log("Generando manual de usuario (puede tardar un momento)...")
                self.master.update_idletasks()
                success, error_msg = create_symlog_manual_pdf(pdf_path)
                if not success:
                    messagebox.showerror("Error al Generar Manual", f"No se pudo crear el manual PDF.\n\nDetalles:\n{error_msg}")
                    self._log(f"ERROR al generar manual: {error_msg}")
                    return
                self._log("Manual generado exitosamente.")
            
            self._log(f"Abriendo manual: {pdf_path}")
            webbrowser.open_new(f"file://{os.path.realpath(pdf_path)}")
        except Exception as e:
            self._log(f"ERROR al abrir manual: {e}")
            messagebox.showerror("Error al Abrir Manual", f"No se pudo abrir el archivo del manual.\n\nError: {e}")

    def _generate_template(self):
        sname = self.selected_scale_name.get()
        if not sname:
            messagebox.showerror("Error","Por favor, selecciona una escala.")
            return
        items = all_scales_data.get(sname)
        if not items:
            self._log(f"Error Interno: No se encontraron ítems para la escala '{sname}'.")
            messagebox.showerror("Error",f"No se encontraron ítems para la escala '{sname}'.")
            return
        sugg = f"plantilla_symlog_{sname.lower().replace(' ', '_')}.xlsx"
        fname = filedialog.asksaveasfilename(defaultextension=".xlsx",initialfile=sugg,filetypes=[("Archivos de Excel","*.xlsx"),("Todos los archivos","*.*")])
        if not fname:
            self._log("Generación de plantilla cancelada por el usuario.")
            return
        self._log(f"Generando plantilla '{sname}' en '{os.path.basename(fname)}'...")
        try:
            item_col="Item SYMLOG (No modificar)"
            p_cols=["Participante_1","Participante_2"]
            texts=[i['item'] for i in items]
            data={item_col:texts}
            for pc in p_cols:
                data[pc] = [0]*len(texts)
            df=pd.DataFrame(data)
            with pd.ExcelWriter(fname, engine='openpyxl') as w:
                 df.to_excel(w, index=False, sheet_name='SYMLOG_Data')
                 ws = w.sheets['SYMLOG_Data']
                 max_l = max(len(str(t)) for t in texts) if texts else 20
                 ws.column_dimensions[ws.cell(1,1).column_letter].width = max(20, max_l + 5)
                 for i, cn in enumerate(p_cols, 2):
                     ws.column_dimensions[ws.cell(1,i).column_letter].width = max(15, len(cn) + 5)
            self._log(f"Plantilla '{os.path.basename(fname)}' guardada exitosamente.")
            messagebox.showinfo("Éxito",f"Plantilla guardada en:\n{fname}")
        except ImportError:
            self._log("ERROR: La librería 'openpyxl' es necesaria para crear archivos Excel.")
            messagebox.showerror("Dependencia Faltante", "Se requiere 'openpyxl' para esta función.\nPor favor, instálala con: pip install openpyxl")
        except Exception as e:
            self._log(f"ERROR al generar plantilla: {e}\n{traceback.format_exc()}")
            messagebox.showerror("Error Crítico",f"Ocurrió un error al generar la plantilla:\n{e}")

    def _update_manual_input_items(self):
        for widget in self.mif.winfo_children():
            widget.destroy()
        self.manual_item_widgets={}
        self.manual_entry_order = []
        scale_name = self.selected_scale_name.get()
        items_list = all_scales_data.get(scale_name) if scale_name else None
        if not items_list:
            ttk.Label(self.mif, text="Por favor, selecciona una escala.").pack(pady=10)
        else:
            self._log(f"Cargando {len(items_list)} ítems para ingreso manual (escala: {scale_name})...")
            validate_cmd = (self.master.register(self._validate_manual_score), '%P')
            try:
                for i, item_data in enumerate(items_list):
                    item_frame = ttk.Frame(self.mif)
                    item_frame.pack(fill=tk.X, pady=2, anchor='nw')
                    item_label = ttk.Label(item_frame, text=f"{i+1}. ({item_data['dimension']}) {item_data['item']}", wraplength=550, justify=tk.LEFT, anchor='w')
                    item_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
                    score_var = tk.StringVar(value='0')
                    score_entry = ttk.Entry(item_frame, textvariable=score_var, width=4, justify=tk.CENTER, validate='key', validatecommand=validate_cmd)
                    score_entry.pack(side=tk.RIGHT, padx=5)
                    self.manual_item_widgets[item_data['item']] = (score_var, score_entry)
                    self.manual_entry_order.append(score_entry)
                    score_entry.bind("<Return>", self._focus_next_entry)
            except Exception as e:
                self._log(f"ERROR CRÍTICO creando widgets manuales: {e}\n{traceback.format_exc()}")
                messagebox.showerror("Error de UI", f"Ocurrió un error al crear los campos de ingreso:\n{e}")
                self._clear_manual_widgets()
                return
        self.master.after_idle(self._configure_manual_scroll)

    def _configure_manual_scroll(self):
        try:
             self.mif.update_idletasks()
             bbox = self.mic.bbox("all")
             if bbox:
                 self.mic.configure(scrollregion=bbox)
                 canvas_width = self.mic.winfo_width()
                 if canvas_width > 1:
                     required_width = bbox[2]
                     self.mic.itemconfig(self.micw, width=max(required_width, canvas_width))
             else:
                 self.mic.configure(scrollregion=(0,0,1,1))
             self.mic.yview_moveto(0)
        except tk.TclError as e:
             self._log(f"Advertencia: Error Tcl al configurar el scroll: {e}")

    def _clear_manual_widgets(self):
        for w in self.mif.winfo_children():
            w.destroy()
        self.manual_item_widgets = {}
        self.manual_entry_order = []
        ttk.Label(self.mif, text="Error al cargar los ítems.").pack()
        self.master.after_idle(self._configure_manual_scroll_after_clear)

    def _configure_manual_scroll_after_clear(self):
        try:
            self.mif.update_idletasks()
            self.mic.configure(scrollregion=(0,0,1,1))
            self.mic.yview_moveto(0)
        except tk.TclError as e:
             self._log(f"Advertencia: Error Tcl al configurar scroll (clear): {e}")

    def _validate_manual_score(self, v):
        return v == "" or (v.isdigit() and 0 <= int(v) <= 4)

    def _focus_next_entry(self, event):
        try:
            current_entry = event.widget
            current_index = self.manual_entry_order.index(current_entry)
            next_index = current_index + 1
            if next_index < len(self.manual_entry_order):
                next_entry = self.manual_entry_order[next_index]
                next_entry.focus_set()
                next_entry.selection_range(0, tk.END)
            else:
                if hasattr(self, 'manual_add_button'):
                    self.manual_add_button.focus_set()
            return "break"
        except ValueError:
            return None
        except Exception as e:
            self._log(f"Error al mover el foco: {e}")
            return None

    def _add_manual(self):
        pname = self.manual_participant_name_entry.get().strip()
        sname = self.selected_scale_name.get()
        if not pname:
            messagebox.showerror("Campo Requerido","Por favor, ingresa un nombre para el participante.")
            return
        if not sname:
            messagebox.showerror("Campo Requerido","Por favor, selecciona una escala.")
            return
            
        self._log(f"Procesando datos manuales para '{pname}' (escala: {sname})...")
        scores = {item: int(svar.get() or 0) for item, (svar, _) in self.manual_item_widgets.items()}
            
        res, ok, msg = calculate_from_manual_scores(pname, sname, scores)
        if msg and msg != "Cálculo manual exitoso.":
            self._log(f"Mensajes del cálculo: {msg}")

        if res:
            self.results_by_scale.setdefault(sname, {'manual': [], 'excel': []})
            mlist = self.results_by_scale[sname].get('manual', [])
            idx = next((i for i, r in enumerate(mlist) if r.get('name','').strip().lower() == pname.strip().lower()), -1)
            
            if idx != -1:
                if messagebox.askyesno("Confirmar Sobrescritura", f"El participante '{pname}' ya existe.\n¿Deseas sobrescribirlo?"):
                    self._log(f"Sobrescribiendo resultados para '{pname}'.")
                    mlist[idx] = res
                else:
                    self._log(f"Adición de '{pname}' cancelada.")
                    return
            else:
                mlist.append(res)
            
            self.results_by_scale[sname]['manual'] = mlist
            self._log(f"Resultados para '{pname}' añadidos/actualizados.")
            self.manual_participant_name_entry.delete(0, tk.END)
            [sv.set('0') for sv, en in self.manual_item_widgets.values()]
            self.manual_participant_name_entry.focus()
            messagebox.showinfo("Éxito", f"Resultados para '{pname}' han sido procesados.")
            self._update_action_panels()
            self._update_widget_states()
        else:
            messagebox.showerror("Error de Cálculo", f"No se pudo calcular el perfil para '{pname}'.\nRevisa los mensajes.")

    def _select_excel(self):
        fpath = filedialog.askopenfilename(title="Seleccionar Archivo Excel", filetypes=[("Archivos de Excel","*.xlsx *.xls"),("Todos los archivos","*.*")])
        if fpath:
            self.selected_excel_file.set(fpath)
            self.excel_file_label.config(text=os.path.basename(fpath), foreground="black")
            self._log(f"Archivo Excel seleccionado: {os.path.basename(fpath)}")
        else:
            self.selected_excel_file.set("")
            self.excel_file_label.config(text="Ningún archivo seleccionado", foreground="grey")
            self._log("Selección de archivo Excel cancelada.")
        self._update_widget_states()

    def _process_excel(self):
        sname = self.selected_scale_name.get()
        fpath = self.selected_excel_file.get()
        if not sname or not fpath:
            messagebox.showerror("Error","Por favor, selecciona una escala y un archivo Excel.")
            return
            
        self._log(f"Procesando '{os.path.basename(fpath)}' para la escala '{sname}'...")
        try:
            df = pd.read_excel(fpath, engine='openpyxl')
            if df.empty:
                messagebox.showerror("Error de Archivo","El archivo Excel seleccionado está vacío."); return
                
            processed_results, warnings = calculate_from_excel(df, sname)
            
            if warnings:
                self._log(f"Se encontraron {len(warnings)} advertencias/errores durante el proceso:")
                for i, w in enumerate(warnings[:15]): self._log(f"  - {w}")
                if len(warnings) > 15: self._log(f"  ... ({len(warnings) - 15} más no mostradas)")
            
            if not processed_results and warnings:
                 messagebox.showerror("Proceso Fallido", "No se pudieron generar perfiles. Revisa los errores en el log y el formato del archivo.")
                 return

            self.results_by_scale.setdefault(sname, {'manual': [], 'excel': []})['excel'] = processed_results
            
            messagebox.showinfo("Proceso Completo", f"Procesamiento de Excel finalizado.\n\nPerfiles generados: {len(processed_results)}\nAdvertencias: {len(warnings)} (revisar log)")
            self._log("--- Fin del Procesamiento de Excel ---")
        except Exception as e:
            self._log(f"ERROR CRÍTICO al procesar Excel: {e}\n{traceback.format_exc()}")
            messagebox.showerror("Error Crítico", f"Ocurrió un error inesperado:\n{e}")
        finally:
            self._update_action_panels()
            self._update_widget_states()

    def _select_json_plot(self):
        fpath = filedialog.askopenfilename(title="Seleccionar Archivo JSON", filetypes=[("Archivos JSON","*.json"),("Todos los archivos","*.*")])
        if fpath:
            self.selected_json_file_plot.set(fpath)
            self.json_plot_file_label.config(text=os.path.basename(fpath), foreground="black")
            self._log(f"JSON seleccionado: {os.path.basename(fpath)}")
        else:
            self.selected_json_file_plot.set("")
            self.json_plot_file_label.config(text="Ningún archivo seleccionado", foreground="grey")
        self._update_widget_states()

    def _generate_and_save_plot(self):
        fname = self.selected_json_file_plot.get()
        if not fname:
            messagebox.showerror("Error", "Por favor, selecciona un archivo JSON."); return
        
        self._log(f"Generando gráfico desde: '{os.path.basename(fname)}'")
        fig = None
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                data = json.load(f)

            scales = list(data.keys())
            if not scales:
                messagebox.showerror("Error de Formato", "El archivo JSON no contiene ninguna escala."); return
            
            scale_to_plot = scales[0]
            if len(scales) > 1:
                 sel = self._ask_scale_selection(scales)
                 if not sel:
                     self._log("Selección de escala cancelada."); return
                 scale_to_plot = sel
            
            participants_data = data.get(scale_to_plot, [])
            if not participants_data:
                messagebox.showwarning("Sin Datos", f"No hay participantes para graficar en la escala '{scale_to_plot}'."); return
                
            fig, ax = plt.subplots(figsize=(11, 8.5))
            has_data = self._draw_symlog_plot(fig, ax, participants_data, scale_to_plot)
            if not has_data:
                messagebox.showwarning("Sin Datos Válidos", "No se pudieron dibujar datos válidos. Revisa el contenido del JSON."); return
                
            def_fname = f"diagrama_symlog_{scale_to_plot.lower().replace(' ', '_')}.png"
            fpath = filedialog.asksaveasfilename(title="Guardar Gráfico SYMLOG", initialfile=def_fname, defaultextension=".png", filetypes=[("Imagen PNG","*.png"),("PDF","*.pdf"),("SVG","*.svg")])
            if not fpath:
                self._log("Guardado de gráfico cancelado."); return
                
            fig.savefig(fpath, dpi=300, bbox_inches='tight')
            self._log(f"¡Gráfico guardado en '{os.path.basename(fpath)}'!")
            messagebox.showinfo("Éxito", f"Gráfico guardado en:\n{fpath}")
            
        except Exception as e:
            self._log(f"ERROR al generar gráfico: {e}\n{traceback.format_exc()}")
            messagebox.showerror("Error Crítico", f"Ocurrió un error inesperado:\n{e}")
        finally:
            if fig: plt.close(fig)

    def _ask_scale_selection(self, scales):
        dialog = tk.Toplevel(self.master)
        dialog.title("Seleccionar Escala")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.master)
        dialog.grab_set()
        
        tk.Label(dialog, text="El archivo contiene múltiples escalas.\nSelecciona cuál deseas graficar:").pack(pady=(10, 5))
        
        sel_var = tk.StringVar(dialog, value=scales[0])
        ttk.Combobox(dialog, textvariable=sel_var, values=scales, state="readonly").pack(pady=5, padx=20, fill=tk.X)
        
        result = None
        def on_ok():
            nonlocal result
            result = sel_var.get()
            dialog.destroy()
            
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Aceptar", command=on_ok).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        
        dialog.wait_window()
        return result

    def _draw_symlog_plot(self, fig, ax, participants_data, scale_name="General"):
        ax.set_title(f"Diagrama de Campo SYMLOG ({scale_name})", fontsize=14, pad=20)
        limit = 20
        ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
        ax.set_aspect('equal', adjustable='box'); ax.grid(True, linestyle='--', alpha=0.6)
        ax.spines['left'].set_position('zero'); ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero'); ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom'); ax.yaxis.set_ticks_position('left')
        tick_step = 4
        ax.set_xticks(np.arange(-limit + tick_step, limit, tick_step))
        ax.set_yticks(np.arange(-limit + tick_step, limit, tick_step))
        ax.tick_params(axis='both', which='major', labelsize=8)
        
        l_off = limit * 0.85; q_props = dict(ha='center', va='center', fontsize=9, color='darkgrey', style='italic')
        ax.text(l_off, l_off, "PF", **q_props); ax.text(-l_off, l_off, "NF", **q_props); ax.text(l_off, -l_off, "PB", **q_props); ax.text(-l_off, -l_off, "NB", **q_props)
        ax_l_off = limit * 0.98; ax_props = dict(ha='center', va='center', fontsize=10, color='black', weight='bold')
        ax.text(ax_l_off, 0, "P", **ax_props); ax.text(-ax_l_off, 0, "N", **ax_props); ax.text(0, ax_l_off, "F", **ax_props); ax.text(0, -ax_l_off, "B", **ax_props)

        n_parts = len(participants_data)
        cmap = plt.get_cmap('tab10' if n_parts <= 10 else 'tab20' if n_parts <= 20 else 'viridis')
        colors = list(cmap.colors) if isinstance(cmap, matplotlib.colors.ListedColormap) else [cmap(i/max(1,n_parts)) for i in range(n_parts)]
        
        plotted, has_data = [], False
        for i, pdat in enumerate(participants_data):
             if isinstance(pdat, dict) and all(k in pdat for k in ['name','pn','fb','ud']) and all(isinstance(pdat.get(k), (int, float)) for k in ['pn','fb','ud']):
                 pn, fb, ud, name = pdat['pn'], pdat['fb'], pdat['ud'], str(pdat.get('name', f'P_{i+1}'))
                 clr = colors[i % len(colors)]
                 size_disp = max(10, calculate_marker_size(ud) / PLOT_SIZE_DIVISOR)
                 ax.scatter(pn, fb, s=size_disp, label=name, alpha=0.8, edgecolors='black', linewidth=0.5, zorder=5, c=[clr])
                 ax.text(pn, fb, name, fontsize=7, zorder=6, ha='center', va='center', bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.6, ec='none'))
                 plotted.append({'name': name, 'color': clr}); has_data = True
             else:
                 self._log(f"Advertencia: Omitiendo participante con datos inválidos: {pdat}")

        if has_data:
             if len(plotted) <= 15:
                 handles = [plt.scatter([], [], s=60, color=p['color'], edgecolors='black', alpha=0.75, label=p['name']) for p in plotted]
                 ax.legend(handles=handles, title="Participantes", bbox_to_anchor=(1.02, 1.0), loc='upper left', fontsize='small')
             
             ref_ud_scores = [18, 0, -18]; ref_labels = [f"U/D = {s}" for s in ref_ud_scores]
             ref_sizes = [max(10, calculate_marker_size(s) / PLOT_SIZE_DIVISOR) for s in ref_ud_scores]
             ref_x = limit + 3.5
             ax.text(ref_x, -1, "Ref. Tamaño (U/D):", ha='center', va='center', fontsize='small', weight='bold')
             for i, score in enumerate(ref_ud_scores):
                 y_pos = [-5, -12, -16][i]
                 ax.scatter([ref_x], [y_pos], s=ref_sizes[i], c='grey', alpha=0.6, edgecolors='black', zorder=4, clip_on=False)
                 ax.text(ref_x, y_pos - (3.5 if score != 0 else 2.5), ref_labels[i], ha='center', va='top', fontsize='small')
             fig.subplots_adjust(left=0.08, bottom=0.08, right=0.78, top=0.90)

        return has_data

    def _save_results(self):
        if not self._has_any_results():
            messagebox.showwarning("Sin Datos", "No hay resultados en la sesión para guardar."); return
        fname = filedialog.asksaveasfilename(defaultextension=".json", initialfile=self.results_filename.get(), filetypes=[("Archivos JSON","*.json")])
        if not fname: return
            
        data = {}
        for sname, sdata in self.results_by_scale.items():
            combined = sdata.get('manual', []) + sdata.get('excel', [])
            if combined:
                 data[sname] = sorted(combined, key=lambda x: x.get('name', '').lower())
        
        if not data:
            messagebox.showerror("Error", "No se encontraron datos válidos para guardar."); return
            
        try:
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            self._log(f"¡Resultados guardados en '{os.path.basename(fname)}'!")
            messagebox.showinfo("Éxito", f"Resultados guardados en:\n{fname}")
            self.results_filename.set(os.path.basename(fname))
        except Exception as e:
            self._log(f"Error al guardar: {e}\n{traceback.format_exc()}")
            messagebox.showerror("Error al Guardar", f"No se pudo escribir en el archivo:\n{e}")

    def _clear_all(self):
        if not self._has_any_results():
            messagebox.showinfo("Info", "No hay resultados para limpiar."); return
            
        if messagebox.askyesno("Confirmar Limpieza", "¿Borrar TODOS los resultados de la sesión actual?"):
             self.results_by_scale = {}
             self._clear_log(); self._log("Todos los resultados de la sesión han sido eliminados.")
             if hasattr(self, 'manual_participant_name_entry'):
                 self.manual_participant_name_entry.delete(0, tk.END)
             if hasattr(self, 'manual_item_widgets'):
                 [v.set('0') for v, e in self.manual_item_widgets.values()]
             self._update_action_panels(); self._update_widget_states()
             messagebox.showinfo("Limpieza Completa", "Resultados eliminados.")

    def _has_any_results(self):
         return any(d.get('manual') or d.get('excel') for d in self.results_by_scale.values())