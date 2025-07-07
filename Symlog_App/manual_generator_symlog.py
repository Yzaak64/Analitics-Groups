# manual_generator_symlog.py (Versión Corregida)

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
import traceback

def create_symlog_manual_pdf(filename="manual_symlog.pdf"):
    """Genera un manual de usuario en formato PDF para la herramienta SYMLOG."""
    try:
        doc = SimpleDocTemplate(filename)
        styles = getSampleStyleSheet()

        # --- Estilos personalizados ---
        styles.add(ParagraphStyle(name='H1', parent=styles['h1'], alignment=TA_CENTER, spaceAfter=20, fontSize=18))
        styles.add(ParagraphStyle(name='H2', parent=styles['h2'], spaceBefore=12, spaceAfter=8, fontSize=14))
        styles.add(ParagraphStyle(name='H3', parent=styles['h3'], spaceBefore=10, spaceAfter=6, fontSize=11))
        styles.add(ParagraphStyle(name='Body', parent=styles['Normal'], alignment=TA_JUSTIFY, spaceAfter=12, leading=14))
        
        # --- CORRECCIÓN: Modificar el estilo 'Bullet' existente en lugar de añadirlo ---
        # Se accede al estilo predefinido 'Bullet' y se ajustan sus propiedades.
        bullet_style = styles['Bullet']
        bullet_style.firstLineIndent = 0
        bullet_style.leftIndent = 18
        bullet_style.spaceAfter = 6
        bullet_style.leading = 14
        # --------------------------------------------------------------------------

        story = []

        # --- Contenido del Manual ---
        story.append(Paragraph("Manual de Usuario: Analizador SYMLOG", styles['H1']))

        story.append(Paragraph("1. Introducción", styles['H2']))
        intro_text = """
        Bienvenido al Analizador SYMLOG. Esta herramienta permite calcular y visualizar perfiles de comportamiento
        grupal basados en el modelo SYMLOG (System for the Multiple Level Observation of Groups). Puede procesar
        datos de las escalas de "Adjetivos" y "Valores", ya sea mediante ingreso manual o importando archivos Excel.
        """
        story.append(Paragraph(intro_text, styles['Body']))
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph("2. Funciones Principales", styles['H2']))
        story.append(Paragraph("La aplicación se organiza en cuatro acciones principales, seleccionables desde el menú desplegable superior:", styles['Body']))

        functions_text = [
            "<b>1. Generar Plantilla Excel:</b> Crea un archivo <code>.xlsx</code> con el formato correcto para ingresar las puntuaciones de los participantes (0-4).",
            "<b>2. Ingresar Datos Manualmente:</b> Permite calificar los 26 ítems para un solo participante y añadirlo a la sesión de resultados.",
            "<b>3. Procesar Archivo Excel Subido:</b> Carga un archivo Excel (previamente generado con la plantilla) y calcula los perfiles de todos los participantes listados en él.",
            "<b>4. Generar Gráfico desde JSON:</b> Carga un archivo <code>.json</code> de resultados (guardado previamente) y genera un Diagrama de Campo SYMLOG."
        ]
        story.append(ListFlowable([ListItem(Paragraph(s, bullet_style)) for s in functions_text], bulletType='bullet', leftIndent=18))
        story.append(Spacer(1, 0.2 * inch))
        
        story.append(Paragraph("3. Flujo de Trabajo Detallado", styles['H2']))

        story.append(Paragraph("3.1. Generar Plantilla Excel", styles['H3']))
        story.append(Paragraph("Esta es la forma recomendada para recolectar datos de múltiples participantes:", styles['Body']))
        template_steps = [
            "Seleccione la acción <b>'1. Generar Plantilla Excel'</b>.",
            "Elija la escala deseada (Adjetivos o Valores).",
            "Haga clic en el botón <b>'Generar y Guardar Plantilla'</b>.",
            "Guarde el archivo <code>.xlsx</code> en su ordenador.",
            "Abra el archivo en Excel. La primera columna contiene los ítems y no debe ser modificada. En las siguientes columnas (P1, P2, etc.), ingrese el nombre de cada participante en el encabezado y sus puntuaciones (de 0 a 4) en las filas correspondientes. Puede añadir tantas columnas de participantes como necesite."
        ]
        story.append(ListFlowable([ListItem(Paragraph(s, bullet_style)) for s in template_steps], bulletType='1', leftIndent=18))

        story.append(Paragraph("3.2. Ingresar Datos Manualmente", styles['H3']))
        story.append(Paragraph("Use esta opción para análisis rápidos o individuales:", styles['Body']))
        manual_steps = [
            "Seleccione la acción <b>'2. Ingresar Datos Manualmente'</b>.",
            "Elija la escala (Adjetivos o Valores).",
            "Ingrese un nombre para el participante.",
            "Rellene los valores (0-4) para cada uno de los 26 ítems. Puede usar la tecla 'Enter' para pasar al siguiente campo.",
            "Haga clic en <b>'Calcular y Añadir'</b> para procesar los datos y agregarlos a los resultados de la sesión."
        ]
        story.append(ListFlowable([ListItem(Paragraph(s, bullet_style)) for s in manual_steps], bulletType='1', leftIndent=18))

        story.append(Paragraph("3.3. Procesar Archivo Excel", styles['H3']))
        story.append(Paragraph("Una vez que tenga su archivo Excel con datos:", styles['Body']))
        excel_steps = [
            "Seleccione la acción <b>'3. Procesar Archivo Excel Subido'</b>.",
            "Elija la escala que corresponde a los datos del archivo.",
            "Haga clic en <b>'Seleccionar Excel'</b> y elija su archivo <code>.xlsx</code>.",
            "Haga clic en <b>'Procesar Excel'</b>. La aplicación calculará los perfiles para todos los participantes en el archivo. Los resultados de esta importación reemplazarán cualquier resultado previo de Excel para la misma escala."
        ]
        story.append(ListFlowable([ListItem(Paragraph(s, bullet_style)) for s in excel_steps], bulletType='1', leftIndent=18))
        
        story.append(PageBreak())

        story.append(Paragraph("4. Resultados y Visualización", styles['H2']))
        story.append(Paragraph(
            "Una vez que haya procesado datos (manual o por Excel), aparecerá un panel de resultados en la parte inferior de la ventana.",
            styles['Body']
        ))
        
        story.append(Paragraph("4.1. Guardar y Limpiar Resultados", styles['H3']))
        results_features = [
            "<b>Guardar Resultados:</b> Le permite guardar todos los resultados calculados en la sesión actual en un único archivo <code>.json</code>. Este archivo es ideal para archivar o para cargarlo más tarde con la opción 'Generar Gráfico desde JSON'.",
            "<b>Limpiar Resultados:</b> Borra todos los datos de la sesión actual."
        ]
        story.append(ListFlowable([ListItem(Paragraph(s, bullet_style)) for s in results_features], bulletType='bullet', leftIndent=18))

        story.append(Paragraph("4.2. Generar Gráfico desde JSON", styles['H3']))
        story.append(Paragraph(
            "Esta opción le permite visualizar datos guardados previamente sin necesidad de recalcularlos. Simplemente seleccione la acción, elija el archivo <code>.json</code> y haga clic en <b>'Generar y Guardar Gráfico'</b>. Podrá guardar el diagrama de campo como una imagen (PNG, PDF, etc.).",
            styles['Body']
        ))

        story.append(Paragraph("4.3. Interpretación del Diagrama de Campo", styles['H3']))
        story.append(Paragraph(
            "El gráfico generado representa a los participantes en un espacio bidimensional:",
            styles['Body']
        ))
        axis_desc = [
            "<b>Eje Horizontal (P-N):</b> Mide la dimensión de Amistoso (Positivo) vs. No Amistoso (Negativo). Los participantes a la derecha son percibidos como más cooperativos y positivos; los de la izquierda, como más negativistas u hostiles.",
            "<b>Eje Vertical (F-B):</b> Mide la dimensión de Orientado a la Tarea (Forward) vs. Orientado a la Emoción (Backward). Los participantes en la parte superior son vistos como más analíticos y centrados en las reglas; los de la parte inferior, como más expresivos y emocionales.",
            "<b>Tamaño del Círculo (U-D):</b> Representa la dimensión de Dominante (Upward) vs. Sumiso (Downward). Círculos más grandes indican un comportamiento más dominante y activo; círculos más pequeños, un comportamiento más pasivo."
        ]
        story.append(ListFlowable([ListItem(Paragraph(s, bullet_style)) for s in axis_desc], bulletType='bullet', leftIndent=18))

        # Construir el PDF
        doc.build(story)
        return True, None
    except Exception as e:
        error_details = traceback.format_exc()
        return False, error_details