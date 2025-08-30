# AnaliticsGroups Suite <a href="https://www.buymeacoffee.com/Yzaak64" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-green.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

**AnaliticsGroups Suite** es un conjunto de herramientas de escritorio desarrolladas en Python para el análisis de dinámicas grupales. La suite unifica tres aplicaciones especializadas en un único lanzador para una experiencia de usuario integrada.

## Aplicaciones Incluidas

La suite se compone de un lanzador principal y tres módulos de análisis:

1.  **Red Sociograma:** Una potente herramienta para la creación, gestión y análisis de datos sociométricos. Permite visualizar las dinámicas de grupo a través de sociogramas interactivos, matrices y dianas de afinidad.
2.  **Cuestionario Hemphill:** Una aplicación dedicada a digitalizar, calificar e interpretar el "Cuestionario de Descripción de Grupos" de J.K. Hemphill, generando perfiles gráficos y tablas de resultados para 13 dimensiones.
3.  **SYMLOG:** Un analizador para calcular y visualizar perfiles de comportamiento grupal basados en el modelo SYMLOG (System for the Multiple Level Observation of Groups), procesando datos de las escalas de "Adjetivos" y "Valores".

## Requisitos del Sistema (para el instalador)

*   Windows 10 o superior.

## Instalación y Uso (Recomendado para Usuarios Finales)

1.  Ve a la sección de [**Releases**](https://github.com/Yzaak64/AnaliticsGroups/releases) de este repositorio. *(Recuerda cambiar la URL si el nombre de tu repositorio es diferente)*.
2.  Descarga el archivo `AnaliticsGroups_Suite_Setup.exe` de la última versión.
3.  Ejecuta el instalador y sigue las instrucciones en pantalla.
4.  Una vez instalado, inicia la suite desde el acceso directo creado en tu escritorio o en el Menú de Inicio.

## Demos Online (Google Colab)

Puedes probar la lógica central de cada aplicación directamente en tu navegador. Estas versiones se enfocan en los cálculos y la generación de gráficos, y no incluyen la interfaz gráfica completa.

*   **Demo de Red Sociograma:**
    [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1D0cQItenmmMBM9mF4oSU6SOUdGvApeHn) Para poder ejecuar este notebook necesitas subir en drive la carpeta llamada "ProgramaSociograma" y asi finalmente poder ejecutar el notebook de Red_Sociograma (v2).

*   **Demo de Cuestionario Hemphill:**
    [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/16CYD5wdEWsZd34SYYGjg1xdC-EM8JEas) Para poder ejecuar este notebook necesitas subir en drive la carpeta llamada "ProgramaHemphill" y asi finalmente poder ejecutar el notebook de Interfaz Hemphill.

*   **Demo de SYMLOG:**
    [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1IUehhFa_ZKf8C6r1WbK-cIpuSbRMRwGO)

*(Es posible que Colab muestre una advertencia de seguridad. Haz clic en "Ejecutar de todos modos" para continuar.)*

## Ejecutar desde el Código Fuente (Para Desarrolladores)

1.  Asegúrate de tener Python 3.9 instalado.
2.  Clona o descarga este repositorio completo.
3.  Abre una terminal en la carpeta raíz del proyecto.
4.  Crea e instala las dependencias en un entorno virtual (recomendado):
    ```bash
    # Navega a la carpeta de cada sub-aplicación y instala sus requisitos
    cd Red_Sociograma_App
    pip install -r requirements.txt
    cd ../Hemphill_App
    pip install -r requirements.txt
    cd ../Symlog_App
    pip install -r requirements.txt
    ```
5.  Vuelve a la carpeta raíz y ejecuta el lanzador principal:
    ```bash
    python AnaliticsGroups.py
    ```

## Generación del Ejecutable e Instalador

Si deseas construir el instalador tú mismo desde el código fuente:

1.  Asegúrate de tener todas las dependencias instaladas.
2.  Instala PyInstaller e Inno Setup:
    *   `pip install pyinstaller`
    *   Descarga e instala [Inno Setup](https://jrsoftware.org/isdl.php).
3.  Navega a la carpeta de cada una de las 4 aplicaciones (`AnaliticsGroups`, `Hemphill_App`, etc.) y ejecuta `pyinstaller <nombre_del_script>.spec` en cada una.
4.  Ensambla la carpeta de distribución final como se describe en el historial de desarrollo.
AnaliticsGroups Suite v1.0/   <---Esta es una Carpeta Nueva que tu creas, las carpetas de abajo tienen que tener esos nombres por lo que ten cuidado con el pyinstaller
|
|-- AnaliticsGroups.exe <---Esta es el archivo de dist dentro de la carpeta AnaliticsGroups
|-- Recursos/ <---Esta es la carpeta que esta en AnaliticsGroups_exe
|-- Hemphill/ <---Esta es la carpeta que esta en dist de Hemphill_App
|-- Red Sociograma/ <---Esta es la carpeta que esta en dist de Red_Sociograma_App
|-- SYMLOG/ <---Esta es la carpeta que esta en dist de Symlog_App
|-- _internal <---Esta es el archivo de dist dentro de la carpeta AnaliticsGroups
5.  Usa Inno Setup para compilar el script del instalador (`.iss`) y generar el `setup.exe` final o ejecuta con esta conformacion AnaliticsGroups.exe.

## Apoya el Proyecto

Si estas herramientas te han sido de utilidad, ¡considera invitar un café para apoyar su desarrollo y mantenimiento futuro! Tu apoyo es muy apreciado.
