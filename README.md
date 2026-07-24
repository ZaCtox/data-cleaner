# Data Cleaner

Herramienta desarrollada en Python para facilitar la limpieza de archivos CSV mediante una interfaz gráfica.

## Funcionalidades

- Seleccionar archivos CSV (codificación y separador detectados automáticamente).
- Mostrar total de registros y columnas.
- Seleccionar qué columnas exportar.
- Renombrar columnas antes de exportar.
- Reordenar columnas con los botones ▲ / ▼.
- Dividir el archivo en 2 a 5 partes.
- Validación de nombres vacíos o duplicados.
- Confirmación antes de sobrescribir archivos existentes.
- Abrir la carpeta `output/` desde la interfaz.

## Requisitos

- Python 3.10 o superior

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/ZaCtox/data_cleaner.git
cd data_cleaner
```

2. Crea y activa un entorno virtual (recomendado):

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

### Desde Python

```bash
python main.py
```

1. Haz clic en **Seleccionar CSV** y elige tu archivo.
2. Marca o desmarca las columnas que quieras conservar.
3. Renombra columnas si lo necesitas.
4. Usa **Seleccionar todo** / **Deseleccionar todo** si lo necesitas.
5. Opcional: activa **Dividir archivo** para generar varias partes.
6. Haz clic en **Procesar**.
7. Usa **Abrir carpeta output** para ver los resultados.

El archivo resultante se guarda en la carpeta `output/` con el nombre `{nombre_original}_limpio.csv`.

### Ejecutable (.exe)

Para generar un `.exe` liviano con solo las dependencias necesarias:

```powershell
.\build.ps1
```

Esto crea un entorno virtual limpio (`.venv-build/`), instala solo `customtkinter` y `pandas`, y compila con PyInstaller.

El ejecutable queda en:

```
dist\DataCleaner.exe
```

Para usarlo, ejecuta:

```powershell
.\dist\DataCleaner.exe
```

Los CSV procesados se guardan en `output/` **junto al .exe** (puedes mover `DataCleaner.exe` a otra carpeta; se creará `output/` ahí).

## Estructura del proyecto

```
data_cleaner/
├── main.py                  # Punto de entrada
├── config.py                # Configuración de la aplicación
├── build.ps1                # Script para generar el .exe
├── DataCleaner.spec         # Configuración PyInstaller
├── ui/
│   └── main_window.py       # Interfaz gráfica
├── processors/
│   └── csv_processor.py     # Lógica de procesamiento CSV
├── models/
│   └── column.py            # Modelo de columna
├── output/                  # Archivos generados (ignorado por git)
└── requirements.txt
```

## Tecnologías

- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
