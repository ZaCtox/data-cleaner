# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Recursos de CustomTkinter (temas e iconos)
datas = collect_data_files("customtkinter")
hiddenimports = collect_submodules("customtkinter")

# Excluir librerías que no usa la app (reduce mucho el tamaño del .exe)
excludes = [
    "matplotlib",
    "scipy",
    "IPython",
    "jupyter",
    "notebook",
    "pytest",
    "PIL",
    "cv2",
    "numba",
    "dask",
    "bokeh",
    "plotly",
    "sklearn",
    "tensorflow",
    "torch",
    "sympy",
    "sphinx",
    "docutils",
    "setuptools",
    "pip",
    "wheel",
    "tkinter.test",
]

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="DataCleaner",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
