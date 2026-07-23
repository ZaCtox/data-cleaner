from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from config import (
    APP_NAME,
    APP_VERSION,
    WINDOW_HEIGHT,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_WIDTH,
)
from models.column import Column
from processors.csv_processor import obtener_info_csv, procesar_csv, procesar_csv_dividido

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_SECTION = ("Segoe UI", 18, "bold")

CSV_FILE_TYPES = [
    ("Archivos CSV", "*.csv"),
    ("Todos los archivos", "*.*"),
]

COLUMNS_FRAME_HEIGHT = 250
DEFAULT_SPLIT_PARTS = "2"


class MainWindow(ctk.CTk):

    # -----------------------------------------------------------------------
    # Inicialización
    # -----------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

        self.configurar_ventana()
        self.inicializar_variables()
        self.crear_layout()
        self.crear_secciones()

    def configurar_ventana(self) -> None:
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

    def inicializar_variables(self) -> None:
        self.ruta_archivo: str | None = None
        self.columnas: list[Column] = []

    def crear_layout(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def crear_secciones(self) -> None:
        self.crear_header()
        self.crear_file_section()
        self.crear_info_section()
        self.crear_columns_section()
        self.crear_footer()

    # -----------------------------------------------------------------------
    # Construcción de interfaz
    # -----------------------------------------------------------------------

    def crear_header(self) -> None:
        self.header_frame = ctk.CTkFrame(self.main_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text=APP_NAME,
            font=FONT_TITLE,
        )
        self.lbl_titulo.grid(row=0, column=0, pady=15)

    def crear_file_section(self) -> None:
        self.file_frame = ctk.CTkFrame(self.main_frame)
        self.file_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.file_frame.grid_columnconfigure(0, weight=1)

        self.btn_archivo = ctk.CTkButton(
            self.file_frame,
            text="Seleccionar CSV",
            command=self.seleccionar_archivo,
        )
        self.btn_archivo.grid(row=0, column=0, pady=(20, 10))

        self.lbl_archivo = ctk.CTkLabel(
            self.file_frame,
            text="Ningún archivo seleccionado",
        )
        self.lbl_archivo.grid(row=1, column=0, pady=(0, 20))

    def crear_info_section(self) -> None:

        self.info_frame = ctk.CTkFrame(self.main_frame)

        self.info_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        self.info_frame.grid_columnconfigure(0, weight=0)
        self.info_frame.grid_columnconfigure(1, weight=0)
        self.info_frame.grid_columnconfigure(2, weight=0)
        self.info_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(
            self.info_frame,
            text="Total de registros:"
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        self.lbl_registros = ctk.CTkLabel(
            self.info_frame,
            text="-"
        )

        self.lbl_registros.grid(
            row=0,
            column=1,
            sticky="w"
        )

        ctk.CTkLabel(
            self.info_frame,
            text="Total de columnas:"
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        self.lbl_columnas = ctk.CTkLabel(
            self.info_frame,
            text="-"
        )

        self.lbl_columnas.grid(
            row=1,
            column=1,
            sticky="w"
        )

        self.chk_dividir = ctk.BooleanVar(value=False)

        self.ck_dividir = ctk.CTkCheckBox(
            self.info_frame,
            text="Dividir archivo",
            variable=self.chk_dividir,
            command=self.cambiar_estado_division
        )

        self.ck_dividir.grid(
            row=2,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        ctk.CTkLabel(
            self.info_frame,
            text="Cantidad:"
        ).grid(
            row=2,
            column=1,
            padx=(5, 5),
            sticky="e"
        )

        self.combo_divisiones = ctk.CTkComboBox(
            self.info_frame,
            values=[str(i) for i in range(2, 6)],
            width=80,
            state="disabled"
        )

        self.combo_divisiones.set("2")

        self.combo_divisiones.grid(
            row=2,
            column=2,
            sticky="w"
        )
        
    def cambiar_estado_division(self) -> None:

        estado = (
            "readonly"
            if self.chk_dividir.get()
            else "disabled"
        )

        self.combo_divisiones.configure(state=estado)

    def crear_columns_section(self) -> None:
        self.columns_frame = ctk.CTkFrame(self.main_frame)
        self.columns_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 15))
        self.columns_frame.grid_columnconfigure(0, weight=1)

        self.lbl_columns = ctk.CTkLabel(
            self.columns_frame,
            text="Columnas encontradas",
            font=FONT_SECTION,
        )
        self.lbl_columns.grid(row=0, column=0, pady=(15, 10))

        self.checkboxes_frame = ctk.CTkScrollableFrame(
            self.columns_frame,
            height=COLUMNS_FRAME_HEIGHT,
        )
        self.checkboxes_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 20),
        )
        self.checkboxes_frame.grid_columnconfigure(0, weight=1)

        self.buttons_frame = ctk.CTkFrame(
            self.columns_frame,
            fg_color="transparent",
        )
        self.buttons_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 20),
        )
        self.buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_seleccionar_todo = ctk.CTkButton(
            self.buttons_frame,
            text="Seleccionar todo",
            command=self.seleccionar_todas,
        )
        self.btn_seleccionar_todo.grid(row=0, column=0, padx=5)

        self.btn_deseleccionar_todo = ctk.CTkButton(
            self.buttons_frame,
            text="Deseleccionar todo",
            command=self.deseleccionar_todas,
        )
        self.btn_deseleccionar_todo.grid(row=0, column=1, padx=5)

        self.btn_procesar = ctk.CTkButton(
            self.buttons_frame,
            text="Procesar",
            command=self.procesar,
        )
        self.btn_procesar.grid(row=0, column=2, padx=5)

    def crear_footer(self) -> None:
        self.footer_frame = ctk.CTkFrame(self.main_frame)
        self.footer_frame.grid(row=4, column=0, sticky="ew")
        self.footer_frame.grid_columnconfigure(1, weight=1)

        self.lbl_estado_titulo = ctk.CTkLabel(
            self.footer_frame,
            text="Estado:",
        )
        self.lbl_estado_titulo.grid(row=0, column=0, padx=20, pady=20)

        self.lbl_estado = ctk.CTkLabel(
            self.footer_frame,
            text="Esperando selección de archivo.",
        )
        self.lbl_estado.grid(row=0, column=1, sticky="w")

    # -----------------------------------------------------------------------
    # Eventos
    # -----------------------------------------------------------------------

    def seleccionar_archivo(self) -> None:
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar CSV",
            filetypes=CSV_FILE_TYPES,
        )

        if not ruta_archivo:
            return

        self.ruta_archivo = ruta_archivo
        self.lbl_archivo.configure(text=Path(ruta_archivo).name)
        self.lbl_estado.configure(text="Leyendo columnas...")

        try:
            info = obtener_info_csv(ruta_archivo)

            self.lbl_registros.configure(text=f"{info['registros']:,}")
            self.lbl_columnas.configure(text=str(len(info["columnas"])))
            self.mostrar_columnas(info["columnas"])
            self.lbl_estado.configure(text="Archivo cargado correctamente.")

        except Exception as error:
            self.ruta_archivo = None
            self.lbl_archivo.configure(text="Ningún archivo seleccionado")
            self.mostrar_columnas([])
            self.lbl_registros.configure(text="-")
            self.lbl_columnas.configure(text="-")
            self.lbl_estado.configure(text=f"Error al leer el archivo: {error}")

    def procesar(self) -> None:

        if self.ruta_archivo is None:
            self.lbl_estado.configure(
                text="Debe seleccionar un archivo CSV."
            )
            return

        columnas = self.obtener_columnas_seleccionadas()
        renombres = self.obtener_renombres()

        if not columnas:
            self.lbl_estado.configure(
                text="Debe seleccionar al menos una columna."
            )
            return

        self.lbl_estado.configure(
            text="Procesando archivo..."
        )

        self.update_idletasks()

        try:

            if self.chk_dividir.get():

                cantidad  = int(
                    self.combo_divisiones.get()
                )

                procesar_csv_dividido(
                    self.ruta_archivo,
                    columnas,
                    renombres,
                    cantidad 
                )

                self.lbl_estado.configure(
                    text=f"Se generaron {cantidad } archivos."
                )

            else:

                ruta_salida = procesar_csv(
                    self.ruta_archivo,
                    columnas,
                    renombres
                )

                self.lbl_estado.configure(
                    text=f"Archivo generado: {ruta_salida.name}"
                )

        except Exception as error:

            self.lbl_estado.configure(
                text=f"Error al procesar: {error}"
            )

    # -----------------------------------------------------------------------
    # Gestión de columnas
    # -----------------------------------------------------------------------

    def mostrar_columnas(self, columnas: list[str]) -> None:
        self.columnas.clear()

        for nombre in columnas:
            self.columnas.append(
                Column(
                    original=nombre,
                    nuevo=nombre,
                    checkbox=ctk.BooleanVar(value=True),
                    entry=ctk.StringVar(value=nombre),
                )
            )

        self.dibujar_columnas()

    def dibujar_columnas(self) -> None:
        for widget in self.checkboxes_frame.winfo_children():
            widget.destroy()

        for fila, columna in enumerate(self.columnas):
            frame = ctk.CTkFrame(self.checkboxes_frame)
            frame.grid(row=fila, column=0, sticky="ew", padx=5, pady=5)
            frame.grid_columnconfigure(2, weight=1)

            checkbox = ctk.CTkCheckBox(
                frame,
                text="",
                variable=columna.checkbox,
                width=25,
            )
            checkbox.grid(row=0, column=0, padx=(10, 5), pady=8)

            lbl = ctk.CTkLabel(
                frame,
                text=columna.original,
                width=180,
                anchor="w",
            )
            lbl.grid(row=0, column=1, sticky="w", padx=5)

            entry = ctk.CTkEntry(frame, textvariable=columna.entry)
            entry.grid(row=0, column=2, sticky="ew", padx=5)

            btn_up = ctk.CTkButton(
                frame,
                text="▲",
                width=35,
                command=lambda i=fila: self.subir_columna(i),
            )
            btn_up.grid(row=0, column=3, padx=(5, 2))

            btn_down = ctk.CTkButton(
                frame,
                text="▼",
                width=35,
                command=lambda i=fila: self.bajar_columna(i),
            )
            btn_down.grid(row=0, column=4, padx=(2, 10))

    def subir_columna(self, indice: int) -> None:
        if indice == 0:
            return

        self.columnas[indice], self.columnas[indice - 1] = (
            self.columnas[indice - 1],
            self.columnas[indice],
        )
        self.dibujar_columnas()

    def bajar_columna(self, indice: int) -> None:
        if indice >= len(self.columnas) - 1:
            return

        self.columnas[indice], self.columnas[indice + 1] = (
            self.columnas[indice + 1],
            self.columnas[indice],
        )
        self.dibujar_columnas()

    def obtener_columnas_seleccionadas(self) -> list[str]:
        return [
            columna.original
            for columna in self.columnas
            if columna.checkbox.get()
        ]

    def seleccionar_todas(self) -> None:
        for columna in self.columnas:
            columna.checkbox.set(True)

    def deseleccionar_todas(self) -> None:
        for columna in self.columnas:
            columna.checkbox.set(False)

    def obtener_renombres(self) -> dict[str, str]:
        return {
            columna.original: columna.entry.get()
            for columna in self.columnas
            if columna.checkbox.get()
        }
