# Changelog

Todos los cambios importantes de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto sigue el versionado semántico.

---

## [0.3.1] - 2026-07-29

### Agregado
- Soporte para importar archivos Excel (.xlsx y .xls).
- Generación de ejecutable mediante `build.ps1`.
- Documentación del proyecto (README).

### Mejorado
- Detección automática de codificación y separador para archivos CSV.
- Validación de nombres de columnas vacíos o duplicados.
- Interfaz de usuario reorganizada.

### Corregido
- Ajustes en el proceso de exportación y generación de archivos.
- Mejor manejo de sobrescritura de archivos existentes.

---

## [0.3.0] - 2026-07-27

### Agregado
- Reordenamiento de columnas mediante botones ▲ y ▼.
- División de archivos entre 2 y 5 partes.
- Información del archivo (cantidad de registros y columnas).

---

## [0.2.0] - 2026-07-26

### Agregado
- Selección de columnas.
- Renombrado de columnas.
- Exportación de archivos CSV limpios.

---

## [0.1.0] - 2026-07-25

### Agregado
- Primera versión funcional de Data Cleaner.
- Interfaz gráfica desarrollada con CustomTkinter.
- Lectura de archivos CSV.