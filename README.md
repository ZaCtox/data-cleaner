# Data Cleaner

Herramienta desarrollada en Python para facilitar la limpieza de archivos CSV mediante una interfaz gráfica.

## Funcionalidades

- Seleccionar archivos CSV.
- Mostrar las columnas disponibles.
- Seleccionar qué columnas exportar.
- Exportar un CSV limpio con las columnas elegidas.

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

1. Ejecuta la aplicación:

```bash
python main.py
```

2. Haz clic en **Seleccionar CSV** y elige tu archivo.
3. Marca o desmarca las columnas que quieras conservar.
4. Usa **Seleccionar todo** o **Deseleccionar todo** si lo necesitas.
5. Haz clic en **Procesar**.

El archivo resultante se guarda en la carpeta `output/` con el nombre `{nombre_original}_limpio.csv`.

## Estructura del proyecto

```
data_cleaner/
├── main.py                  # Punto de entrada
├── config.py                # Configuración de la aplicación
├── ui/
│   └── main_window.py       # Interfaz gráfica
├── processors/
│   └── csv_processor.py     # Lógica de procesamiento CSV
├── output/                  # Archivos generados (ignorado por git)
└── requirements.txt
```

## Tecnologías

- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
