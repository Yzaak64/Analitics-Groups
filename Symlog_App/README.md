
# Aplicación de Interfaz Gráfica SYMLOG Tkinter <a href="https://www.buymeacoffee.com/Yzaak64" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-green.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

Esta es una aplicación de escritorio desarrollada con Python y Tkinter para facilitar el cálculo y la visualización de resultados según la metodología SYMLOG.

## Características

*   **Generación de Plantillas:** Crea archivos Excel (.xlsx) con el formato adecuado para ingresar puntuaciones SYMLOG (escalas "Adjetivos" y "Valores").
*   **Entrada Manual:** Permite ingresar directamente los puntajes (0-4) para cada ítem de una escala seleccionada para un participante específico, con navegación mediante la tecla Enter.
*   **Procesamiento de Excel:** Carga y procesa archivos Excel que siguen el formato de la plantilla generada, calculando los puntajes SYMLOG (UD, PN, FB) para múltiples participantes.
*   **Guardado de Resultados:** Almacena los resultados calculados (tanto manuales como de Excel) en un archivo JSON estructurado por escala.
*   **Visualización Gráfica:** Genera un diagrama de campo SYMLOG (gráfico PN vs FB) a partir de un archivo JSON de resultados previamente guardado. Los puntos se colorean por participante y su tamaño varía según la dimensión UD. Incluye leyendas para participantes y referencia de tamaño manual.
*   **Interfaz Amigable:** Utiliza Tkinter y ttk para una interfaz de usuario clara.

## Requisitos (para ejecutar desde el código fuente)

*   Python 3.x
*   Librerías listadas en `requirements.txt`. Puedes instalarlas usando pip:
    ```bash
    pip install -r requirements.txt
    ```
    Las principales dependencias son:
    *   `pandas`
    *   `openpyxl`
    *   `matplotlib`
    *   `numpy`

## Uso

**Opción 1: Ejecutar desde el Código Fuente (Localmente)**

1.  Asegúrate de tener Python y las librerías requeridas instaladas (ver sección Requisitos).
2.  Clona o descarga este repositorio.
3.  Abre una terminal o símbolo del sistema en la carpeta del proyecto.
4.  Ejecuta el script principal:
    ```bash
    python symblog.py
    ```
5.  Sigue las opciones en la interfaz gráfica que aparecerá.

**Opción 2: Usar el Ejecutable (Windows)**

1.  Ve a la sección [**Releases**](https://github.com/Yzaak64/SYMLOG/releases) de este repositorio.
2.  Descarga el archivo `SYMLOG_App.exe` de la última versión disponible.
3.  Guarda el archivo en tu computadora.
4.  Haz doble clic en el archivo `.exe` para iniciar la aplicación. No requiere instalación de Python ni librerías adicionales.

**Opción 3: Probar en Google Colab (Demo Online)**

1.  Haz clic en el siguiente enlace para abrir una versión del núcleo de la aplicación directamente en tu navegador usando Google Colab:
    [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1IUehhFa_ZKf8C6r1WbK-cIpuSbRMRwGO?usp=sharing)
    *(O copia y pega esta URL: `https://colab.research.google.com/drive/1IUehhFa_ZKf8C6r1WbK-cIpuSbRMRwGO?usp=sharing`)*
2.  Es posible que Colab muestre una advertencia indicando que el cuaderno no fue creado por Google. Haz clic en "Run anyway" o "Ejecutar de todos modos".
3.  Ejecuta las celdas de código (puedes usar "Runtime" > "Run all" en el menú, o ejecutar cada celda individualmente con Shift+Enter).
4.  **Nota:** Esta versión de Colab se enfoca en la lógica de cálculo y la generación del gráfico. **El gráfico se mostrará directamente en el cuaderno** en lugar de guardarse en un archivo. Las funciones que dependen de la interfaz gráfica de Tkinter (como la selección interactiva de archivos o la entrada manual directa en la GUI) no estarán disponibles en Colab.

## Generación del Ejecutable (Instrucciones para desarrollador)

Si deseas crear el archivo `.exe` tú mismo desde el código fuente:

1.  Asegúrate de tener Python y las librerías de `requirements.txt` instaladas en tu entorno.
2.  Instala PyInstaller: `pip install pyinstaller`
3.  Navega a la carpeta raíz del proyecto en tu terminal.
4.  Asegúrate de que el archivo de ícono `Symlog.ico` esté presente en esa misma carpeta.
5.  Ejecuta el siguiente comando:
    ```bash
    pyinstaller --name="SYMLOG_App" --onefile --windowed --icon="Symlog.ico" --clean symblog.py
    ```
6.  El ejecutable (`SYMLOG_App.exe`) se encontrará en la subcarpeta `dist` que se creará.

## Notas

*   El cálculo de puntajes desde Excel asume que las filas en el archivo están en el mismo orden que los ítems definidos internamente para la escala seleccionada. La primera columna debe contener los ítems (aunque no se usa directamente para el cálculo) y las columnas siguientes los puntajes de cada participante.
*   La generación de gráficos carga los datos desde un archivo JSON previamente guardado por la aplicación (cuando se usa localmente o el ejecutable).
