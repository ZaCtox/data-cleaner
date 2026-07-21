from pathlib import Path

import pandas as pd

from config import OUTPUT_DIR


def obtener_columnas(ruta_archivo: str) -> list[str]:
    """
    Obtiene los nombres de las columnas del CSV.
    """
    df = pd.read_csv(ruta_archivo, nrows=0)
    return df.columns.tolist()


def procesar_csv(
    ruta_archivo: str,
    columnas: list[str]
) -> Path:
    """
    Genera un nuevo CSV manteniendo únicamente
    las columnas seleccionadas.
    """
    df = pd.read_csv(ruta_archivo)
    df = df[columnas]

    ruta_salida = (
        OUTPUT_DIR /
        f"{Path(ruta_archivo).stem}_limpio.csv"
    )

    df.to_csv(
        ruta_salida,
        index=False,
        encoding="utf-8-sig"
    )

    return ruta_salida
