# ===================================================================================
# manual_generator.py (VERSIÓN 2 - CORREGIDA)
# Contiene la lógica para generar el manual de usuario en PDF.
# ===================================================================================

print("--- Ejecutando manual_generator.py v2 (La versión corregida sin el error 'Bullet') ---")

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import traceback

def create_manual_pdf(filename="manual_hemphill.pdf"):
    """Genera un manual de usuario en formato PDF."""
    try:
        doc = SimpleDocTemplate(filename)
        styles = getSampleStyleSheet()

        # --- Estilos personalizados (línea conflictiva eliminada) ---
        styles.add(ParagraphStyle(name='H1', parent=styles['h1'], alignment=TA_CENTER, spaceAfter=20, fontSize=18))
        styles.add(ParagraphStyle(name='H2', parent=styles['h2'], spaceBefore=12, spaceAfter=8, fontSize=14))
        styles.add(ParagraphStyle(name='H3', parent=styles['h3'], spaceBefore=10, spaceAfter=6, fontSize=11))
        styles.add(ParagraphStyle(name='Body', parent=styles['Normal'], alignment=TA_JUSTIFY, spaceAfter=12, leading=14))
        
        story = []

        # --- Contenido del PDF ---
        title = "Manual de Usuario: Analizador de Cuestionario Hemphill"
        story.append(Paragraph(title, styles['H1']))

        story.append(Paragraph("1. Introducción", styles['H2']))
        intro_text = """
        Bienvenido al Analizador de Cuestionario Hemphill. Esta herramienta está diseñada para digitalizar y simplificar 
        el proceso de calificación e interpretación del Cuestionario de Descripción de Grupos de Hemphill. Permite tanto 
        el ingreso manual de respuestas como el procesamiento masivo de datos a través de archivos CSV, generando 
        perfiles gráficos y tablas de resultados para un análisis profundo.
        """
        story.append(Paragraph(intro_text, styles['Body']))
        story.append(Spacer(1, 0.2*inch))

        story.append(Paragraph("2. Cómo Crear un Archivo de Importación con Google Forms", styles['H2']))
        story.append(Paragraph(
            "Una de las formas más eficientes de recolectar datos es a través de un formulario en línea. A continuación, se detalla cómo configurar un formulario en Google Forms para que sea 100% compatible con este programa.",
            styles['Body']
        ))
        
        steps = [
            "<b>Paso 1: Crear el Formulario.</b> Vaya a Google Forms y cree un nuevo formulario en blanco. Asígnele un título, como 'Cuestionario de Descripción de Grupos'.",
            "<b>Paso 2: Añadir la Pregunta de Identificación.</b> La primera pregunta <b>debe ser</b> para identificar al participante. Use el tipo 'Lista Desplegable', escriba 'Nombre del Participante o Grupo:' y márquela como obligatoria.",
            "<b>Paso 3: Añadir las 150 Preguntas del Cuestionario.</b> Para cada una de las 150 afirmaciones, añada una nueva pregunta de tipo <b>'Escala lineal o Opcion Multiple'</b>. Configure el rango de <b>1 a 5</b>. En las etiquetas, escriba 'Totalmente de acuerdo' para el 1 y 'Nada de acuerdo' para el 5. En el caso de Opcion Multiple deben estar como '1 - TOTALMENTE DE ACUERDO, 2 - BASTANTE DE ACUERDO, 3 - REGULAR, 4 - POCO DE ACUERDO, 5 - NADA DE ACUERDO' (incluyendo el numero). Copie el texto de la afirmación en el título de la pregunta y márquela como obligatoria.",
            "<b>Paso 4: Recolectar y Exportar.</b> Una vez recibidas las respuestas, vaya a la pestaña 'Respuestas' y haga clic en el icono verde de 'Crear hoja de cálculo'. En la hoja de cálculo, vaya a <b>Archivo > Descargar > Valores separados por comas (.csv)</b>. Este archivo CSV es el que importará en el programa."
        ]
        for step in steps:
            story.append(Paragraph(step, styles['Bullet']))
        
        story.append(PageBreak())
        
        story.append(Paragraph("3. Guía de Uso del Programa", styles['H2']))

        story.append(Paragraph("3.1 Pantalla de Inicio", styles['H3']))
        story.append(Paragraph("La pantalla principal le ofrece las siguientes opciones:", styles['Body']))
        options = [
            "<b>📝 Responder Cuestionario Manualmente:</b> Para ingresar las respuestas de un solo participante directamente en la aplicación.",
            "<b>📂 Procesar Respuestas del Cuestionario:</b> Para cargar archivos CSV (ej. de Google Forms) que contienen las respuestas numéricas de los participantes.",
            "<b>📊 Procesar Puntuaciones Crudas:</b> Para usuarios avanzados que ya han calculado las puntuaciones crudas y solo desean convertirlas a estaninas y graficarlas.",
            "<b>💾 Descargar Plantillas:</b> Para obtener archivos CSV de ejemplo que puede llenar manualmente.",
            "<b>📖 Ver Manual de Instrucciones:</b> Abre o descarga este manual."
        ]
        for opt in options:
            story.append(Paragraph(opt, styles['Bullet']))

        story.append(Paragraph("3.2 Cuestionario Manual", styles['H3']))
        story.append(Paragraph("Este modo le guía paso a paso. Primero, se le pedirá un nombre o identificador. Luego, responderá cada una de las 150 preguntas. Al finalizar, si todas las preguntas están completas, se le mostrará la pantalla de resultados con su perfil individual.", styles['Body']))

        story.append(Paragraph("3.3 Procesamiento de Archivos (CSV)", styles['H3']))
        story.append(Paragraph("Permite analizar múltiples participantes a la vez. El programa generará un perfil para cada participante encontrado en los archivos y calculará un promedio grupal.", styles['Body']))

        story.append(Paragraph("3.4 Pantalla de Resultados", styles['H3']))
        story.append(Paragraph("Esta es la pantalla principal de análisis:", styles['Body']))
        results_features = [
            "<b>Menú Desplegable:</b> Permite seleccionar qué resultado ver. Si procesó varios participantes, aparecerá la opción 'Promedio Grupal'.",
            "<b>Tabla de Resultados:</b> Muestra los valores numéricos de las puntuaciones crudas y estaninas.",
            "<b>Gráfico de Perfil:</b> Visualiza las puntuaciones estaninas en un gráfico de barras, con bandas de color para una interpretación rápida (Bajo, Promedio, Alto).",
            "<b>Exportar Vista Actual:</b> Guarda un CSV de lo que está viendo actualmente (perfil individual o promedio grupal).",
            "<b>Exportar Datos Consolidados:</b> Crea un único archivo CSV con todos los resultados, ideal para análisis estadísticos externos."
        ]
        for feat in results_features:
            story.append(Paragraph(feat, styles['Bullet']))

        # --- Construir el PDF ---
        doc.build(story)
        return True
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! ERROR AL GENERAR EL PDF. DETALLE DEL PROBLEMA: !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if create_manual_pdf():
        print("Manual 'manual_hemphill.pdf' creado con éxito.")
    else:
        print("Error al crear el manual.")