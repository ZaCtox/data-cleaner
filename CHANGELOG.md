# Changelog

Todos los cambios importantes de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto sigue el versionado semántico.

---

## [0.4.0] - 2026-08-18

### Agregado
- Nuevo modo de procesamiento Genérico.
- El modo Genérico selecciona automáticamente las columnas nombre, email y token.
- Orden automático de las columnas nombre, email y token en el modo Genérico.
- Validación de columnas requeridas antes de activar el modo Genérico.
- Nuevo modo Personalizado para mantener el control manual sobre selección, renombrado y orden de columnas.
- Selector de modo de procesamiento mediante botones de opción.

### Mejorado
- Los controles de selección, renombrado y reordenamiento se bloquean automáticamente cuando se utiliza el modo Genérico.
- La división de archivos entre 2 y 5 partes está disponible tanto en modo Genérico como Personalizado.
- El estado del procesamiento muestra la cantidad de archivos generados.
- La interfaz reorganiza las opciones de procesamiento antes de la configuración de columnas.

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