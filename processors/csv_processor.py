from pathlib import Path
from typing import TypedDict
import csv

import pandas as pd

from config import CSV_ENCODINGS_TO_TRY, OUTPUT_DIR, OUTPUT_ENCODING


class CsvInfo(TypedDict):
    registros: int
    columnas: list[str]


class ValidationError(ValueError):
    """Error de validación de columnas o renombres."""


def detectar_encoding(ruta_archivo: str) -> str:
    """Prueba codificaciones comunes hasta encontrar una válida."""
    muestra = Path(ruta_archivo).read_bytes()[:8192]

    for encoding in CSV_ENCODINGS_TO_TRY:
        try:
            muestra.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue

    raise ValueError("No se pudo detectar la codificación del archivo.")


def detectar_separador(ruta_archivo: str, encoding: str) -> str:
    """Detecta el separador de columnas (coma, punto y coma o tabulador)."""
    with open(ruta_archivo, encoding=encoding, newline="") as archivo:
        muestra = archivo.read(8192)

    if not muestra.strip():
        return ","

    try:
        dialecto = csv.Sniffer().sniff(muestra, delimiters=",;\t")
        return dialecto.delimiter
    except csv.Error:
        return ","


def validar_renombres(renombres: dict[str, str]) -> None:
    nombres = [nombre.strip() for nombre in renombres.values()]

    if any(not nombre for nombre in nombres):
        raise ValidationError("Los nombres de columna no pueden estar vacíos.")

    if len(set(nombres)) != len(nombres):
        raise ValidationError("Hay nombres de columna duplicados.")


def cargar_csv(ruta_archivo: str) -> tuple[CsvInfo, pd.DataFrame]:
    """Carga el CSV detectando codificación y separador automáticamente."""
    encoding = detectar_encoding(ruta_archivo)
    separador = detectar_separador(ruta_archivo, encoding)

    df = pd.read_csv(ruta_archivo, encoding=encoding, sep=separador)

    info: CsvInfo = {
        "registros": len(df),
        "columnas": df.columns.tolist(),
    }

    return info, df


def _preparar_dataframe(
    df: pd.DataFrame,
    columnas: list[str],
    renombres: dict[str, str],
) -> pd.DataFrame:
    validar_renombres(renombres)

    faltantes = set(columnas) - set(df.columns)
    if faltantes:
        raise ValidationError(
            f"Columnas no encontradas: {', '.join(sorted(faltantes))}"
        )

    resultado = df[columnas].copy()
    return resultado.rename(columns=renombres)


def rutas_salida_esperadas(
    ruta_origen: str,
    cantidad_partes: int = 1,
) -> list[Path]:
    stem = Path(ruta_origen).stem

    if cantidad_partes == 1:
        return [OUTPUT_DIR / f"{stem}_limpio.csv"]

    return [
        OUTPUT_DIR / f"{stem}_limpio_{i}.csv"
        for i in range(1, cantidad_partes + 1)
    ]


def procesar_csv(
    df: pd.DataFrame,
    ruta_origen: str,
    columnas: list[str],
    renombres: dict[str, str],
    sobrescribir: bool = False,
) -> Path:
    """Genera un CSV con las columnas seleccionadas y renombres aplicados."""
    resultado = _preparar_dataframe(df, columnas, renombres)

    ruta_salida = rutas_salida_esperadas(ruta_origen)[0]

    if ruta_salida.exists() and not sobrescribir:
        raise FileExistsError(
            f"El archivo ya existe: {ruta_salida.name}. "
            "Confirma la sobrescritura para continuar."
        )

    resultado.to_csv(
        ruta_salida,
        index=False,
        encoding=OUTPUT_ENCODING,
    )

    return ruta_salida


def procesar_csv_dividido(
    df: pd.DataFrame,
    ruta_origen: str,
    columnas: list[str],
    renombres: dict[str, str],
    cantidad_partes: int,
    sobrescribir: bool = False,
) -> list[Path]:
    """Genera varios CSV dividiendo el archivo en partes."""
    if cantidad_partes < 2:
        raise ValidationError(
            "La cantidad de partes debe ser mayor o igual a 2."
        )

    resultado = _preparar_dataframe(df, columnas, renombres)
    rutas_esperadas = rutas_salida_esperadas(ruta_origen, cantidad_partes)

    if not sobrescribir:
        existentes = [ruta.name for ruta in rutas_esperadas if ruta.exists()]
        if existentes:
            raise FileExistsError(
                "Ya existen archivos de salida: "
                f"{', '.join(existentes)}. "
                "Confirma la sobrescritura para continuar."
            )

    total_registros = len(resultado)
    filas_base = total_registros // cantidad_partes
    sobrantes = total_registros % cantidad_partes

    rutas_generadas: list[Path] = []
    inicio = 0

    for i, ruta_salida in enumerate(rutas_esperadas):
        filas = filas_base + (1 if i < sobrantes else 0)
        fin = inicio + filas

        parte = resultado.iloc[inicio:fin]
        parte.to_csv(
            ruta_salida,
            index=False,
            encoding=OUTPUT_ENCODING,
        )

        rutas_generadas.append(ruta_salida)
        inicio = fin

    return rutas_generadas
