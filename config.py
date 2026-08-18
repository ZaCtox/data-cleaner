import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Proyecto
# ---------------------------------------------------------------------------


def _get_base_dir() -> Path:
    """Directorio base: carpeta del .exe empaquetado o del proyecto."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


BASE_DIR = _get_base_dir()

# ---------------------------------------------------------------------------
# Carpetas
# ---------------------------------------------------------------------------

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Aplicación
# ---------------------------------------------------------------------------

APP_NAME = "Data Cleaner"
APP_VERSION = "0.4.0"

# ---------------------------------------------------------------------------
# Ventana
# ---------------------------------------------------------------------------

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------

CSV_ENCODINGS_TO_TRY = [
    "utf-8-sig",
    "utf-8",
    "cp1252",
    "latin-1",
]

DEFAULT_SPLIT_PARTS = "2"
OUTPUT_ENCODING = "utf-8-sig"
