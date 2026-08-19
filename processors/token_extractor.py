from pathlib import Path
import re

import pandas as pd

from config import OUTPUT_DIR, OUTPUT_ENCODING


def extraer_token(texto: object) -> str:
    if pd.isna(texto):
        return ""

    texto = str(texto)

    coincidencia = re.search(
        r"/token/([^?&#/]+)",
        texto
    )

    if coincidencia:
        return coincidencia.group(1)

    return ""


def generar_archivo_tokens(
    df: pd.DataFrame,
    ruta_origen: str,
    columna_numero: str,
    columna_enlace: str,
    sobrescribir: bool = False,
) -> Path:

    if columna_numero not in df.columns:
        raise ValueError(
            f"No existe la columna: {columna_numero}"
        )

    if columna_enlace not in df.columns:
        raise ValueError(
            f"No existe la columna: {columna_enlace}"
        )

    resultado = pd.DataFrame({
        "numero": df[columna_numero],
        "token": df[columna_enlace].apply(extraer_token),
    })

    ruta_salida = (
        OUTPUT_DIR /
        f"{Path(ruta_origen).stem}_tokens.csv"
    )

    if ruta_salida.exists() and not sobrescribir:
        raise FileExistsError(
            f"El archivo ya existe: {ruta_salida.name}"
        )

    resultado.to_csv(
        ruta_salida,
        index=False,
        encoding=OUTPUT_ENCODING,
    )

    return ruta_salida