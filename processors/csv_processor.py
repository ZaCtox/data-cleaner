from pathlib import Path
from typing import TypedDict

import pandas as pd

from config import OUTPUT_DIR


class CsvInfo(TypedDict):
    registros: int
    columnas: list[str]


def obtener_info_csv(ruta_archivo: str) -> CsvInfo:
    """
    Obtiene información básica del CSV.
    """
    df = pd.read_csv(ruta_archivo)

    return {
        "registros": len(df),
        "columnas": df.columns.tolist(),
    }


def procesar_csv(
    ruta_archivo: str,
    columnas: list[str],
    renombres: dict[str, str],
) -> Path:
    """
    Genera un nuevo CSV manteniendo únicamente
    las columnas seleccionadas y aplicando renombres.
    """
    df = pd.read_csv(ruta_archivo)
    df = df[columnas]
    df = df.rename(columns=renombres)

    ruta_salida = OUTPUT_DIR / f"{Path(ruta_archivo).stem}_limpio.csv"

    df.to_csv(
        ruta_salida,
        index=False,
        encoding="utf-8-sig",
    )

    return ruta_salida

def procesar_csv_dividido(
    ruta_archivo: str,
    columnas: list[str],
    renombres: dict[str, str],
    cantidad_partes: int,
) -> None:
    """
    Genera varios CSV dividiendo el archivo
    en la cantidad de partes indicada.
    """

    if cantidad_partes < 2:
        raise ValueError(
            "La cantidad de partes debe ser mayor o igual a 2."
        )

    df = pd.read_csv(ruta_archivo)

    df = df[columnas]
    df = df.rename(columns=renombres)

    total_registros = len(df)

    filas_base = total_registros // cantidad_partes
    sobrantes = total_registros % cantidad_partes

    inicio = 0

    for i in range(cantidad_partes):

        filas = filas_base

        if i < sobrantes:
            filas += 1

        fin = inicio + filas

        parte = df.iloc[inicio:fin]

        ruta_salida = (
            OUTPUT_DIR /
            f"{Path(ruta_archivo).stem}_limpio_{i+1}.csv"
        )

        parte.to_csv(
            ruta_salida,
            index=False,
            encoding="utf-8-sig"
        )

        inicio = fin