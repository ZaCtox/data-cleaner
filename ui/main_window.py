from pathlib import Path
import os
import threading
from tkinter import filedialog, messagebox

import customtkinter as ctk
import pandas as pd

from config import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_SPLIT_PARTS,
    OUTPUT_DIR,
    WINDOW_HEIGHT,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_WIDTH,
)
from models.column import Column
from processors.csv_processor import (
    ValidationError,
    cargar_archivo,
    rutas_salida_esperadas,
    procesar_csv,
    procesar_csv_dividido,
    validar_renombres,
)
from processors.token_extractor import generar_archivo_tokens
# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_SECTION = ("Segoe UI", 18, "bold")

DATA_FILE_TYPES = [
    ("Todos los archivos", "*.*"),
    ("Archivos CSV", "*.csv"),
    ("Archivos Excel", "*.xlsx"),
    ("Archivos Excel 97-2003", "*.xls"),
]

COLUMNS_FRAME_HEIGHT = 250


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
        self.df: pd.DataFrame | None = None
        self.columnas: list[Column] = []
        self.modo_procesamiento = ctk.StringVar(value="personalizado")
        self.procesando = False
        self.ultimas_rutas: list[Path] = []
        
        # Variables para la sección de token
        self.ruta_archivo_token: str | None = None
        self.df_token: pd.DataFrame | None = None

    def crear_layout(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Contenedor principal de toda la aplicación
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.main_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=20,
            pady=20
        )

        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Header general
        self.crear_header()

        # Pestañas
        self.tabview = ctk.CTkTabview(
            self.main_frame
        )

        self.tabview.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # Crear pestañas
        self.tab_preparar = self.tabview.add(
            "Preparar archivo"
        )

        self.tab_tokens = self.tabview.add(
            "Extraer token"
        )

        # Configurar pestaña Preparar archivo
        self.tab_preparar.grid_columnconfigure(
            0,
            weight=1
        )

        self.tab_preparar.grid_rowconfigure(
            3,
            weight=1
        )

        # Configurar pestaña Extraer token
        self.tab_tokens.grid_columnconfigure(
            0,
            weight=1
        )

    def crear_secciones(self) -> None:
        self.crear_file_section()
        self.crear_info_section()
        self.crear_modo_section()
        self.crear_columns_section()
        self.crear_footer()

        self.crear_token_section()

    # -----------------------------------------------------------------------
    # Construcción de interfaz
    # -----------------------------------------------------------------------

    def crear_header(self) -> None:
        self.header_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        self.header_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text=APP_NAME,
            font=FONT_TITLE,
        )

        self.lbl_titulo.grid(
            row=0,
            column=0,
            pady=15
        )

    def crear_file_section(self) -> None:
        self.file_frame = ctk.CTkFrame(self.tab_preparar)
        self.file_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.file_frame.grid_columnconfigure(0, weight=1)

        self.btn_archivo = ctk.CTkButton(
            self.file_frame,
            text="Seleccionar archivo",
            command=self.seleccionar_archivo,
        )
        self.btn_archivo.grid(row=0, column=0, pady=(20, 10))

        self.lbl_archivo = ctk.CTkLabel(
            self.file_frame,
            text="Ningún archivo seleccionado",
        )
        self.lbl_archivo.grid(row=1, column=0, pady=(0, 20))

    def crear_info_section(self) -> None:
        self.info_frame = ctk.CTkFrame(self.tab_preparar)
        self.info_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.info_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(self.info_frame, text="Total de registros:").grid(
            row=0, column=0, padx=15, pady=10, sticky="w"
        )

        self.lbl_registros = ctk.CTkLabel(self.info_frame, text="-")
        self.lbl_registros.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(self.info_frame, text="Total de columnas:").grid(
            row=1, column=0, padx=15, pady=10, sticky="w"
        )

        self.lbl_columnas = ctk.CTkLabel(self.info_frame, text="-")
        self.lbl_columnas.grid(row=1, column=1, sticky="w")

        self.chk_dividir = ctk.BooleanVar(value=False)

        self.ck_dividir = ctk.CTkCheckBox(
            self.info_frame,
            text="Dividir archivo",
            variable=self.chk_dividir,
            command=self.cambiar_estado_division,
        )
        self.ck_dividir.grid(row=2, column=0, padx=15, pady=15, sticky="w")

        ctk.CTkLabel(self.info_frame, text="Cantidad:").grid(
            row=2, column=1, padx=(5, 5), sticky="e"
        )

        self.combo_divisiones = ctk.CTkComboBox(
            self.info_frame,
            values=[str(i) for i in range(2, 6)],
            width=80,
            state="disabled",
        )
        self.combo_divisiones.set(DEFAULT_SPLIT_PARTS)
        self.combo_divisiones.grid(row=2, column=2, sticky="w")

    def cambiar_estado_division(self) -> None:
        estado = "normal" if self.chk_dividir.get() else "disabled"
        self.combo_divisiones.configure(state=estado)
        
    def crear_modo_section(self) -> None:

        self.modo_frame = ctk.CTkFrame(self.tab_preparar)

        self.modo_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 15),
        )

        self.modo_frame.grid_columnconfigure((0, 1), weight=1)

        titulo = ctk.CTkLabel(
            self.modo_frame,
            text="Modo de procesamiento",
            font=FONT_SECTION,
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(15, 10),
        )

        self.radio_generico = ctk.CTkRadioButton(
            self.modo_frame,
            text="Genérico",
            variable=self.modo_procesamiento,
            value="generico",
            command=self.cambiar_modo,
        )

        self.radio_generico.grid(
            row=1,
            column=0,
            padx=20,
            pady=(5, 15),
        )

        self.radio_personalizado = ctk.CTkRadioButton(
            self.modo_frame,
            text="Personalizado",
            variable=self.modo_procesamiento,
            value="personalizado",
            command=self.cambiar_modo,
        )

        self.radio_personalizado.grid(
            row=1,
            column=1,
            padx=20,
            pady=(5, 15),
        )
        
    def crear_columns_section(self) -> None:
        self.columns_frame = ctk.CTkFrame(self.tab_preparar)
        self.columns_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 15))
        self.columns_frame.grid_columnconfigure(0, weight=1)
        self.columns_frame.grid_rowconfigure(1, weight=1)

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
        self.buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

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

        self.btn_abrir_output = ctk.CTkButton(
            self.buttons_frame,
            text="Abrir carpeta output",
            command=self.abrir_carpeta_output,
            state="disabled",
        )
        self.btn_abrir_output.grid(row=0, column=3, padx=5)

    def crear_footer(self) -> None:
        self.footer_frame = ctk.CTkFrame(self.tab_preparar)
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
        
    def crear_token_section(self) -> None:

        self.token_file_frame = ctk.CTkFrame(
            self.tab_tokens
        )

        self.token_file_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=15
        )

        self.token_file_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.btn_token_archivo = ctk.CTkButton(
            self.token_file_frame,
            text="Seleccionar archivo",
            command=self.seleccionar_archivo_token
        )

        self.btn_token_archivo.grid(
            row=0,
            column=0,
            pady=(15, 10)
        )

        self.lbl_token_archivo = ctk.CTkLabel(
            self.token_file_frame,
            text="Ningún archivo seleccionado"
        )

        self.lbl_token_archivo.grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

        self.token_config_frame = ctk.CTkFrame(
            self.tab_tokens
        )

        self.token_config_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            self.token_config_frame,
            text="Columna número:"
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        self.combo_token_numero = ctk.CTkComboBox(
            self.token_config_frame,
            values=[],
            state="disabled"
        )

        self.combo_token_numero.grid(
            row=0,
            column=1,
            padx=15,
            pady=10,
            sticky="w"
        )

        ctk.CTkLabel(
            self.token_config_frame,
            text="Columna enlace:"
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        self.combo_token_enlace = ctk.CTkComboBox(
            self.token_config_frame,
            values=[],
            state="disabled"
        )

        self.combo_token_enlace.grid(
            row=1,
            column=1,
            padx=15,
            pady=10,
            sticky="w"
        )

        self.btn_generar_tokens = ctk.CTkButton(
            self.token_config_frame,
            text="Generar archivo",
            command=self.procesar_tokens,
            state="disabled"
        )

        self.btn_generar_tokens.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=15
        )

        self.lbl_token_estado = ctk.CTkLabel(
            self.tab_tokens,
            text="Esperando selección de archivo."
        )

        self.lbl_token_estado.grid(
            row=2,
            column=0,
            pady=10
        )
        
        
    # -----------------------------------------------------------------------
    # Eventos
    # -----------------------------------------------------------------------

    def cambiar_modo(self) -> None:

        if self.modo_procesamiento.get() == "generico":
            self.aplicar_modo_generico()
        else:
            self.habilitar_modo_personalizado()

        self.dibujar_columnas()

        if self.modo_procesamiento.get() == "generico":
            self.btn_seleccionar_todo.configure(state="disabled")
            self.btn_deseleccionar_todo.configure(state="disabled")
        else:
            self.btn_seleccionar_todo.configure(state="normal")
            self.btn_deseleccionar_todo.configure(state="normal")


    def aplicar_modo_generico(self) -> None:

        columnas_genericas = ["nombre", "email", "token"]

        disponibles = {
            columna.original.lower(): columna
            for columna in self.columnas
        }

        faltantes = [
            nombre
            for nombre in columnas_genericas
            if nombre not in disponibles
        ]

        if faltantes:
            self.lbl_estado.configure(
                text=(
                    "Modo Genérico no disponible. "
                    f"Faltan columnas: {', '.join(faltantes)}"
                )
            )

            self.modo_procesamiento.set("personalizado")
            return

        # Desmarcar todas
        for columna in self.columnas:
            columna.checkbox.set(False)

        seleccionadas = []

        # Seleccionar y ordenar nombre, email, token
        for nombre in columnas_genericas:

            columna = disponibles[nombre]

            columna.checkbox.set(True)
            columna.entry.set(nombre)

            seleccionadas.append(columna)

        restantes = [
            columna
            for columna in self.columnas
            if columna not in seleccionadas
        ]

        self.columnas = seleccionadas + restantes

        self.lbl_estado.configure(
            text="Modo Genérico aplicado: nombre, email y token."
        )


    def habilitar_modo_personalizado(self) -> None:

        self.lbl_estado.configure(
            text="Modo Personalizado activado."
        )

    def seleccionar_archivo(self) -> None:
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=DATA_FILE_TYPES,
        )

        if not ruta_archivo:
            return

        self.ruta_archivo = ruta_archivo
        self.lbl_archivo.configure(text=Path(ruta_archivo).name)
        self.lbl_estado.configure(text="Leyendo archivo...")
        self._habilitar_controles(False)

        def worker() -> None:
            try:
                info, df = cargar_archivo(ruta_archivo)
                self.after(0, lambda: self._on_archivo_cargado(info, df))
            except Exception as error:
                self.after(0, lambda: self._on_archivo_error(str(error)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_archivo_cargado(self, info: dict, df: pd.DataFrame) -> None:
        self.df = df
        self.lbl_registros.configure(text=f"{info['registros']:,}")
        self.lbl_columnas.configure(text=str(len(info["columnas"])))
        self.mostrar_columnas(info["columnas"])
        if self.modo_procesamiento.get() == "generico":
            self.aplicar_modo_generico()
            self.dibujar_columnas()
        self.lbl_estado.configure(text="Archivo cargado correctamente.")
        self._habilitar_controles(True)

    def _on_archivo_error(self, mensaje: str) -> None:
        self.ruta_archivo = None
        self.df = None
        self.lbl_archivo.configure(text="Ningún archivo seleccionado")
        self.mostrar_columnas([])
        self.lbl_registros.configure(text="-")
        self.lbl_columnas.configure(text="-")
        self.lbl_estado.configure(text=f"Error al leer el archivo: {mensaje}")
        self._habilitar_controles(True)

    def seleccionar_archivo_token(self) -> None:

        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=DATA_FILE_TYPES,
        )

        if not ruta_archivo:
            return

        self.ruta_archivo_token = ruta_archivo

        self.lbl_token_archivo.configure(
            text=Path(ruta_archivo).name
        )

        self.lbl_token_estado.configure(
            text="Leyendo archivo..."
        )

        try:
            info, df = cargar_archivo(ruta_archivo)

            self.df_token = df

            columnas = info["columnas"]

            self.combo_token_numero.configure(
                values=columnas,
                state="readonly"
            )

            self.combo_token_enlace.configure(
                values=columnas,
                state="readonly"
            )

            if columnas:
                self.combo_token_numero.set(
                    columnas[0]
                )

                self.combo_token_enlace.set(
                    columnas[-1]
                )

            self.btn_generar_tokens.configure(
                state="normal"
            )

            self.lbl_token_estado.configure(
                text=f"{info['registros']:,} registros cargados."
            )

        except Exception as error:

            self.df_token = None

            self.lbl_token_estado.configure(
                text=f"Error: {error}"
            )

    def procesar_tokens(self) -> None:

        if (
            self.df_token is None
            or self.ruta_archivo_token is None
        ):
            return

        columna_numero = (
            self.combo_token_numero.get()
        )

        columna_enlace = (
            self.combo_token_enlace.get()
        )

        try:
            ruta = generar_archivo_tokens(
                self.df_token,
                self.ruta_archivo_token,
                columna_numero,
                columna_enlace
            )

            self.lbl_token_estado.configure(
                text=f"Archivo generado: {ruta.name}"
            )

        except FileExistsError:

            confirmar = messagebox.askyesno(
                "Archivo existente",
                "El archivo ya existe. ¿Deseas sobrescribirlo?"
            )

            if not confirmar:
                return

            ruta = generar_archivo_tokens(
                self.df_token,
                self.ruta_archivo_token,
                columna_numero,
                columna_enlace,
                sobrescribir=True
            )

            self.lbl_token_estado.configure(
                text=f"Archivo generado: {ruta.name}"
            )

        except Exception as error:

            self.lbl_token_estado.configure(
                text=f"Error: {error}"
            )

    def procesar(self) -> None:
        if self.procesando:
            return

        if self.ruta_archivo is None or self.df is None:
            self.lbl_estado.configure(text="Debe seleccionar un archivo.")
            return

        columnas = self.obtener_columnas_seleccionadas()
        renombres = self.obtener_renombres()

        if not columnas:
            self.lbl_estado.configure(text="Debe seleccionar al menos una columna.")
            return

        try:
            validar_renombres(renombres)
        except ValidationError as error:
            self.lbl_estado.configure(text=str(error))
            return

        dividir = self.chk_dividir.get()
        cantidad = int(self.combo_divisiones.get()) if dividir else 1

        rutas_esperadas = rutas_salida_esperadas(
            self.ruta_archivo,
            cantidad if dividir else 1,
        )
        existentes = [ruta for ruta in rutas_esperadas if ruta.exists()]

        sobrescribir = False
        if existentes:
            nombres = ", ".join(ruta.name for ruta in existentes)
            confirmar = messagebox.askyesno(
                "Archivos existentes",
                f"Ya existen estos archivos:\n{nombres}\n\n¿Deseas sobrescribirlos?",
            )
            if not confirmar:
                self.lbl_estado.configure(text="Procesamiento cancelado.")
                return
            sobrescribir = True

        self.procesando = True
        self.lbl_estado.configure(text="Procesando archivo...")
        self._habilitar_controles(False)

        df = self.df
        ruta_archivo = self.ruta_archivo

        def worker() -> None:
            try:
                if dividir:
                    rutas = procesar_csv_dividido(
                        df,
                        ruta_archivo,
                        columnas,
                        renombres,
                        cantidad,
                        sobrescribir=sobrescribir,
                    )
                    self.after(0, lambda: self._on_proceso_ok_dividido(rutas))
                else:
                    ruta = procesar_csv(
                        df,
                        ruta_archivo,
                        columnas,
                        renombres,
                        sobrescribir=sobrescribir,
                    )
                    self.after(0, lambda: self._on_proceso_ok(ruta))
            except Exception as error:
                self.after(0, lambda: self._on_proceso_error(str(error)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_proceso_ok(self, ruta: Path) -> None:
        self.procesando = False
        self.ultimas_rutas = [ruta]
        self.lbl_estado.configure(text=f"Archivo generado: {ruta.name}")
        self.btn_abrir_output.configure(state="normal")
        self._habilitar_controles(True)

    def _on_proceso_ok_dividido(self, rutas: list[Path]) -> None:
        self.procesando = False
        self.ultimas_rutas = rutas
        self.lbl_estado.configure(text=f"Se generaron {len(rutas)} archivos.")
        self.btn_abrir_output.configure(state="normal")
        self._habilitar_controles(True)

    def _on_proceso_error(self, mensaje: str) -> None:
        self.procesando = False
        self.lbl_estado.configure(text=f"Error al procesar: {mensaje}")
        self._habilitar_controles(True)

    def abrir_carpeta_output(self) -> None:
        os.startfile(OUTPUT_DIR)

    def _habilitar_controles(self, habilitado: bool) -> None:
        estado = "normal" if habilitado else "disabled"

        self.btn_archivo.configure(state=estado)
        self.btn_procesar.configure(state=estado)
        self.btn_seleccionar_todo.configure(state=estado)
        self.btn_deseleccionar_todo.configure(state=estado)
        self.ck_dividir.configure(state=estado)

        if self.chk_dividir.get():
            self.combo_divisiones.configure(state=estado)
        else:
            self.combo_divisiones.configure(state="disabled")

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
        es_generico = self.modo_procesamiento.get() == "generico"
        estado = "disabled" if es_generico else "normal"
        
        for fila, columna in enumerate(self.columnas):
            frame = ctk.CTkFrame(self.checkboxes_frame)
            frame.grid(row=fila, column=0, sticky="ew", padx=5, pady=5)
            frame.grid_columnconfigure(2, weight=1)

            checkbox = ctk.CTkCheckBox(
                frame,
                text="",
                variable=columna.checkbox,
                width=25,
                state=estado,
            )
            checkbox.grid(row=0, column=0, padx=(10, 5), pady=8)

            lbl = ctk.CTkLabel(
                frame,
                text=columna.original,
                width=180,
                anchor="w",
            )
            lbl.grid(row=0, column=1, sticky="w", padx=5)

            entry = ctk.CTkEntry(frame, textvariable=columna.entry, state=estado)
            entry.grid(row=0, column=2, sticky="ew", padx=5)

            btn_up = ctk.CTkButton(
                frame,
                text="▲",
                width=35,
                state=estado,
                command=lambda i=fila: self.subir_columna(i),
            )
            btn_up.grid(row=0, column=3, padx=(5, 2))

            btn_down = ctk.CTkButton(
                frame,
                text="▼",
                width=35,
                state=estado,
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
            columna.original: columna.entry.get().strip()
            for columna in self.columnas
            if columna.checkbox.get()
        }
