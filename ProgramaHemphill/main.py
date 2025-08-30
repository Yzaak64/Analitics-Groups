# ===================================================================================
# main.py (PARA COLAB)
# Archivo principal que contiene la interfaz interactiva.
# ===================================================================================

import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output, Javascript
from google.colab import files
import io

# Importar lógica y datos de los otros archivos del proyecto
from config import preguntas_espanol, nombres_dimensiones
from logic import calculate_scores_from_answers, calculate_stanine
from manual_generator import create_manual_pdf

# Contenedor principal para toda la interfaz
main_container = widgets.VBox()

# Variables globales para el estado del cuestionario manual
current_question_index = 0
all_answers = []

def show_start_screen(b=None):
    """Muestra la pantalla de inicio con todas las opciones."""
    start_new_button = widgets.Button(description="📝 Responder Cuestionario Manualmente", button_style='info', layout=widgets.Layout(width='auto'))
    upload_question_button = widgets.Button(description="📂 Procesar Respuestas del Cuestionario (CSV)", layout=widgets.Layout(width='auto'))
    upload_scores_button = widgets.Button(description="📊 Procesar Puntuaciones Crudas (CSV)", layout=widgets.Layout(width='auto'))
    download_template_button = widgets.Button(description="💾 Descargar Plantillas", icon='download')
    
    manual_button = widgets.Button(description="📖 Generar y Descargar Manual (PDF)", icon='book', layout=widgets.Layout(width='auto'))
    
    # Asignar funciones a los clics de los botones
    manual_button.on_click(generate_and_download_manual)
    start_new_button.on_click(start_new_quiz)
    upload_question_button.on_click(lambda b: process_files_setup('questions'))
    upload_scores_button.on_click(lambda b: process_files_setup('scores'))
    download_template_button.on_click(show_template_download_options)
    
    # Construir la vista de inicio
    main_container.children = [widgets.VBox([
        widgets.HTML("<h2>Analizador de Cuestionario Hemphill</h2><p>Selecciona una opción:</p>"),
        manual_button,
        start_new_button,
        upload_question_button,
        upload_scores_button,
        download_template_button
    ])]

def generate_and_download_manual(b=None):
    """Primero genera el PDF usando el código y luego lo descarga."""
    filename = "manual_hemphill.pdf"
    print("⚙️ Generando el manual de instrucciones, por favor espera...")
    
    try:
        # Paso 1: Intentar crear el PDF
        success = create_manual_pdf(filename)
        
        # Paso 2: Si se creó con éxito, descargarlo
        if success:
            print(f"✅ Manual '{filename}' generado con éxito.")
            print("🚀 ¡Iniciando descarga! Revisa la carpeta de descargas de tu navegador.")
            files.download(filename)
        else:
            # El error detallado ya se imprimió dentro de create_manual_pdf
            print("❌ No se pudo generar el archivo del manual. Revisa la traza de error de arriba.")
            
    except Exception as e:
        print(f"❌ ERROR INESPERADO: Ocurrió un problema durante el proceso.")
        print(f"   Detalle del error: {e}")

def show_template_download_options(b=None):
    """Muestra los botones para descargar las plantillas CSV."""
    download_q_button = widgets.Button(description="Plantilla de Respuestas (150 preguntas)")
    download_s_button = widgets.Button(description="Plantilla de Puntuaciones Crudas")
    back_button = widgets.Button(description="⬅️ Volver")
    back_button.on_click(show_start_screen)
    
    def on_download_questions_click(b):
        download_template('questions')
    def on_download_scores_click(b):
        download_template('scores')

    download_q_button.on_click(on_download_questions_click)
    download_s_button.on_click(on_download_scores_click)
    
    main_container.children = [widgets.VBox([
        widgets.HTML("<h3>Descargar Plantillas</h3><p>Selecciona la plantilla que deseas descargar.</p>"),
        download_q_button,
        download_s_button,
        back_button
    ])]

def download_template(mode):
    """Genera y descarga un archivo de plantilla CSV."""
    print(f"⚙️ Generando plantilla para '{mode}'...")
    try:
        if mode == 'questions':
            headers = ["Nombre:"] + [f"{p}" for p in preguntas_espanol]
            df = pd.DataFrame(columns=headers)
            df.loc[0] = ["Ejemplo Sujeto 1"] + ["1"]*150
            df.loc[1] = ["# Escriba las respuestas (números del 1 al 5) en las columnas siguientes"] + [""]*150
        else: # mode == 'scores'
            headers = ["Nombre o Identificador del Sujeto/Grupo:"] + [f"Puntuación Cruda para: {nombres_dimensiones[d]}" for d in nombres_dimensiones.keys()]
            df = pd.DataFrame(columns=headers)
            df.loc[0] = ["Ejemplo Grupo Alfa"] + [20]*13
            df.loc[1] = ["# Escriba las puntuaciones crudas (números) en las columnas siguientes"] + [""]*13
            
        filename = f"plantilla_{mode}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ Archivo '{filename}' creado correctamente. Iniciando descarga...")
        files.download(filename)
    except Exception as e:
        print(f"❌ ERROR: No se pudo generar o descargar el archivo. Detalle: {e}")

def start_new_quiz(b=None):
    """Inicia el flujo del cuestionario manual, pidiendo primero el nombre."""
    
    def display_quiz_view(participant_name):
        """Muestra la interfaz del cuestionario una vez que se tiene el nombre."""
        global all_answers, current_question_index
        all_answers = [0] * 150
        current_question_index = 0
        
        instruction_label = widgets.HTML(
            value="""<h3>Instrucciones</h3>
            <p>Lee cada afirmación y responde según tu grado de acuerdo o desacuerdo, usando los siguientes números:</p>
            <ul>
                <li><b>1:</b> Totalmente de acuerdo</li>
                <li><b>2:</b> De acuerdo</li>
                <li><b>3:</b> Indeciso</li>
                <li><b>4:</b> En desacuerdo</li>
                <li><b>5:</b> Totalmente en desacuerdo</li>
            </ul>
            <p>Puedes presionar 'Enter' para pasar a la siguiente pregunta.</p>"""
        )
        quiz_question_label = widgets.HTML()
        quiz_answer_input = widgets.Text(placeholder='Escribe 1-5')
        quiz_feedback_label = widgets.HTML()
        prev_button = widgets.Button(description="⬅️ Anterior")
        next_button = widgets.Button(description="Siguiente ➡️", button_style='primary')
        finish_button = widgets.Button(description="🏁 Finalizar", button_style='success')
        quiz_back_button = widgets.Button(description="❌ Salir", button_style='danger')
        quiz_back_button.on_click(show_start_screen)
        
        def update_view(index):
            global current_question_index
            current_question_index = index
            quiz_question_label.value = f"<h3>Pregunta {index + 1}/150</h3><p style='font-size: 1.1em;'>{preguntas_espanol[index]}</p>"
            quiz_answer_input.value = str(all_answers[index]) if all_answers[index] != 0 else ""
            prev_button.disabled = (index == 0)
            next_button.disabled = (index == 149)
            display(Javascript("document.querySelector('input[placeholder=\"Escribe 1-5\"]').focus()"))
            display(Javascript("document.querySelector('input[placeholder=\"Escribe 1-5\"]').setAttribute('maxlength', '1');"))

        def save_current_answer():
            try:
                val = quiz_answer_input.value
                if not val:
                    all_answers[current_question_index] = 0
                    return True
                num = int(val)
                if 1 <= num <= 5:
                    all_answers[current_question_index] = num
                    quiz_feedback_label.value = ""
                    return True
                else:
                    quiz_feedback_label.value = "<p style='color:red;'><b>Error:</b> El número debe estar entre 1 y 5.</p>"
                    return False
            except ValueError:
                quiz_feedback_label.value = "<p style='color:red;'><b>Error:</b> Por favor, introduce solo un número.</p>"
                return False

        def on_nav(direction):
            if save_current_answer():
                new_index = current_question_index + (1 if direction == 'next' else -1)
                if 0 <= new_index < 150:
                    update_view(new_index)
        
        def on_finish():
            if not save_current_answer():
                return
            if 0 in all_answers:
                first_unanswered = all_answers.index(0)
                update_view(first_unanswered)
                quiz_feedback_label.value = f"<p style='color:red;'><b>Atención:</b> Falta por responder la pregunta #{first_unanswered + 1}.</p>"
                return
            show_results_screen({participant_name: calculate_scores_from_answers(all_answers)})

        quiz_answer_input.on_submit(lambda s: on_nav('next') if current_question_index < 149 else on_finish())
        next_button.on_click(lambda b: on_nav('next'))
        prev_button.on_click(lambda b: on_nav('prev'))
        finish_button.on_click(lambda b: on_finish())

        main_container.children = [widgets.VBox([
            instruction_label,
            quiz_question_label,
            quiz_answer_input,
            quiz_feedback_label,
            widgets.HBox([prev_button, next_button]),
            widgets.HBox([quiz_back_button, finish_button])
        ])]
        update_view(0)

    # --- Pantalla para pedir el nombre ---
    name_input = widgets.Text(placeholder="Ej: Grupo Alfa, Juan Pérez", description="Nombre:", layout=widgets.Layout(width='400px'))
    start_quiz_button = widgets.Button(description="Comenzar Cuestionario ➡️", button_style='success', icon='play')
    back_button = widgets.Button(description="⬅️ Volver")
    back_button.on_click(show_start_screen)

    def on_start_quiz_click(b):
        name = name_input.value.strip()
        if not name:
            name = "Sujeto Anónimo"
        display_quiz_view(name)

    start_quiz_button.on_click(on_start_quiz_click)

    main_container.children = [widgets.VBox([
        widgets.HTML("<h2>Responder Cuestionario</h2><p>Por favor, introduce un nombre o identificador para este análisis.</p>"),
        name_input,
        widgets.HBox([back_button, start_quiz_button])
    ])]

def process_files_setup(mode):
    """Prepara la interfaz para la subida de archivos."""
    upload_widget = widgets.FileUpload(accept='.csv', multiple=True, description="Seleccionar Archivos")
    back_button = widgets.Button(description="⬅️ Volver")
    back_button.on_click(show_start_screen)
    
    def on_upload(change):
        process_uploaded_files(change.new, mode)
    
    upload_widget.unobserve_all()
    upload_widget.observe(on_upload, names='value')
    
    main_container.children = [widgets.VBox([
        widgets.HTML(f"<h3>Procesar { 'Respuestas' if mode == 'questions' else 'Puntuaciones'}</h3>"),
        upload_widget,
        back_button
    ])]

def process_uploaded_files(uploaded_files, mode):
    """Procesa los archivos CSV subidos por el usuario."""
    all_individual_results = {}
    output_area = widgets.Output()
    back_button = widgets.Button(description="⬅️ Volver al Inicio")
    back_button.on_click(show_start_screen)
    main_container.children = [widgets.VBox([output_area, back_button])]
    
    with output_area:
        print("Procesando archivos...")
        for filename, data in uploaded_files.items():
            try:
                content = data['content']
                try:
                    decoded_content = content.decode('utf-8')
                except UnicodeDecodeError:
                    decoded_content = content.decode('latin1')
                df_raw = pd.read_csv(io.StringIO(decoded_content), header=0)

                if mode == 'questions':
                    name_col = next((col for col in df_raw.columns if "Nombre" in col), None)
                    if not name_col:
                        print(f"AVISO: El archivo '{filename}' fue omitido por no tener una columna de 'Nombre'.")
                        continue
                    start_index = df_raw.columns.get_loc(name_col) + 1
                    for idx, row in df_raw.iterrows():
                        base_name = row[name_col] if pd.notna(row[name_col]) and str(row[name_col]).strip() else "Sujeto"
                        nombre = f"{base_name}_{idx+1}"
                        respuestas = [int(str(r).strip().split(' ')[0]) for r in row[start_index : start_index + 150]]
                        all_individual_results[nombre] = calculate_scores_from_answers(respuestas)
                else: # mode == 'scores'
                    name_col = 'Nombre o Identificador del Sujeto/Grupo:'
                    if name_col not in df_raw.columns:
                        print(f"AVISO: El archivo '{filename}' fue omitido por no tener la columna '{name_col}'.")
                        continue
                    for idx, row in df_raw.iterrows():
                        base_name = row[name_col] if pd.notna(row[name_col]) and str(row[name_col]).strip() else "Sujeto"
                        nombre = f"{base_name}_{idx+1}"
                        puntuaciones_brutas = {key: row[f"Puntuación Cruda para: {val}"] for key, val in nombres_dimensiones.items()}
                        all_individual_results[nombre] = calculate_stanine(puntuaciones_brutas)
            except Exception as e:
                print(f"Error procesando '{filename}': {e}")
        
        if all_individual_results:
            show_results_screen(all_individual_results)
        else:
            print("No se pudieron procesar archivos válidos o no se seleccionó ningún archivo.")

def show_results_screen(results_dict):
    """Muestra la pantalla de resultados con tablas y gráficos."""
    all_dfs = [df.assign(Sujeto=name) for name, df in results_dict.items()]
    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_df['Puntuación Estanina'] = pd.to_numeric(combined_df['Puntuación Estanina'], errors='coerce')
    average_df = combined_df.groupby('Dimensión')['Puntuación Estanina'].mean().round(2).reset_index()
    average_df.rename(columns={'Puntuación Estanina': 'Promedio Estanina'}, inplace=True)
    
    dropdown_options = (["Promedio Grupal"] + list(results_dict.keys())) if len(results_dict) > 1 else list(results_dict.keys())
    initial_view = dropdown_options[0] if dropdown_options else ""

    view_selector = widgets.Dropdown(options=dropdown_options, value=initial_view, description="Ver:")
    table_output = widgets.Output()
    plot_output = widgets.Output()
    export_view_button = widgets.Button(description="Exportar Vista", icon='table')
    export_all_button = widgets.Button(description="Exportar Todo", icon='database')
    back_to_start_button = widgets.Button(description="🏠 Inicio")
    back_to_start_button.on_click(show_start_screen)

    def update_view(change):
        selected = change['new']
        with table_output:
            clear_output(wait=True)
            if selected == "Promedio Grupal":
                display(average_df)
            elif selected in results_dict:
                display(results_dict[selected])
        with plot_output:
            clear_output(wait=True)
            fig, ax = plt.subplots(figsize=(10, 8))
            df_to_plot = average_df.copy() if selected == "Promedio Grupal" else results_dict[selected].copy()
            value_col = 'Promedio Estanina' if selected == "Promedio Grupal" else 'Puntuación Estanina'
            title = 'Perfil Grupal Promediado' if selected == "Promedio Grupal" else f'Perfil Individual: {selected}'
            color = 'rebeccapurple' if selected == "Promedio Grupal" else 'darkcyan'
            dimension_order = [nombres_dimensiones[d] for d in nombres_dimensiones.keys()]
            df_to_plot['Dimensión'] = pd.Categorical(df_to_plot['Dimensión'], categories=dimension_order, ordered=True)
            df_to_plot = df_to_plot.sort_values('Dimensión')
            df_to_plot[value_col] = pd.to_numeric(df_to_plot[value_col], errors='coerce').fillna(0)
            bars = ax.barh(df_to_plot['Dimensión'], df_to_plot[value_col], color=color)
            ax.set_xlabel('Puntuación Estanina'); ax.set_title(title, fontsize=16)
            ax.set_xticks(range(1, 10)); ax.set_xlim(0, 10)
            for bar in bars:
                width = bar.get_width()
                if width > 0: ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.2f}', ha='left', va='center')
            ax.fill_betweenx(ax.get_ylim(), 0, 3.5, color='red', alpha=0.1, label='Bajo (1-3)')
            ax.fill_betweenx(ax.get_ylim(), 3.5, 6.5, color='grey', alpha=0.1, label='Promedio (4-6)')
            ax.fill_betweenx(ax.get_ylim(), 6.5, 10, color='green', alpha=0.1, label='Alto (7-9)')
            ax.legend(title='Interpretación', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout(rect=[0, 0, 0.85, 1]); plt.show()
            
    def on_export_view(b):
        selected = view_selector.value
        df_export = average_df if selected == "Promedio Grupal" else results_dict[selected]
        filename = "resultados_promedio_grupal.csv" if selected == "Promedio Grupal" else f"resultados_{selected}.csv"
        df_export.to_csv(filename, index=False, encoding='utf-8-sig'); files.download(filename)
        
    def on_export_all(b):
        consolidated_df = combined_df.pivot(index='Sujeto', columns='Dimensión', values='Puntuación Estanina')
        consolidated_df.to_csv('datos_consolidados.csv', encoding='utf-8-sig'); files.download('datos_consolidados.csv')
    
    view_selector.observe(update_view, names='value')
    export_view_button.on_click(on_export_view)
    export_all_button.on_click(on_export_all)
    
    main_container.children = [widgets.VBox([
        widgets.HTML("<h2>Resultados del Análisis</h2>"),
        view_selector,
        table_output,
        plot_output,
        widgets.HBox([export_view_button, export_all_button, back_to_start_button])
    ])]
    if initial_view:
        update_view({'new': initial_view})

# --- Lanzador Principal de la App ---
show_start_screen()
display(main_container)