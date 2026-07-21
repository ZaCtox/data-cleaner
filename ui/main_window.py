import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path

from processors.csv_processor import (
    obtener_columnas,
    procesar_csv
)
from config import (
    APP_NAME,
    APP_VERSION,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT
)

class MainWindow(ctk.CTk):

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self) -> None:
        super().__init__()

        self.configurar_ventana()
        self.inicializar_variables()
        self.crear_layout()
        self.crear_secciones()

    # =====================================================
    # Configuración
    # =====================================================

    def configurar_ventana(self) -> None:

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

    def inicializar_variables(self) -> None:

        self.ruta_archivo: str | None = None

        # nombre_columna -> BooleanVar
        self.columnas_disponibles: dict[str, ctk.BooleanVar] = {}

    def crear_layout(self) -> None:

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

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

        self.main_frame.grid_columnconfigure(0, weight=1)

    def crear_secciones(self) -> None:

        self.crear_header()
        self.crear_file_section()
        self.crear_columns_section()
        self.crear_footer()

    # =====================================================
    # Interfaz
    # =====================================================

    def crear_header(self) -> None:

        self.header_frame = ctk.CTkFrame(self.main_frame)

        self.header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        self.header_frame.grid_columnconfigure(0, weight=1)

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text=APP_NAME,
            font=("Segoe UI", 26, "bold")
        )

        self.lbl_titulo.grid(
            row=0,
            column=0,
            pady=15
        )

    def crear_file_section(self) -> None:

        self.file_frame = ctk.CTkFrame(self.main_frame)

        self.file_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        self.file_frame.grid_columnconfigure(0, weight=1)

        self.btn_archivo = ctk.CTkButton(
            self.file_frame,
            text="Seleccionar CSV",
            command=self.seleccionar_archivo
        )

        self.btn_archivo.grid(
            row=0,
            column=0,
            pady=(20, 10)
        )

        self.lbl_archivo = ctk.CTkLabel(
            self.file_frame,
            text="Ningún archivo seleccionado"
        )

        self.lbl_archivo.grid(
            row=1,
            column=0,
            pady=(0, 20)
        )

    def crear_columns_section(self) -> None:

        self.columns_frame = ctk.CTkFrame(self.main_frame)

        self.columns_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            pady=(0, 15)
        )

        self.columns_frame.grid_columnconfigure(0, weight=1)

        self.lbl_columns = ctk.CTkLabel(
            self.columns_frame,
            text="Columnas encontradas",
            font=("Segoe UI", 18, "bold")
        )

        self.lbl_columns.grid(
            row=0,
            column=0,
            pady=(15, 10)
        )

        self.checkboxes_frame = ctk.CTkScrollableFrame(
            self.columns_frame,
            height=250
        )

        self.checkboxes_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 20)
        )

        self.checkboxes_frame.grid_columnconfigure(0, weight=1)
        
        self.buttons_frame = ctk.CTkFrame(
            self.columns_frame,
            fg_color="transparent"
        )

        self.buttons_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 20)
        )

        self.buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)       
        
        self.btn_seleccionar_todo = ctk.CTkButton(
            self.buttons_frame,
            text="Seleccionar todo",
            command=self.seleccionar_todas
        )

        self.btn_seleccionar_todo.grid(
            row=0,
            column=0,
            padx=5
        ) 

        self.btn_deseleccionar_todo = ctk.CTkButton(
            self.buttons_frame,
            text="Deseleccionar todo",
            command=self.deseleccionar_todas
        )

        self.btn_deseleccionar_todo.grid(
            row=0,
            column=1,
            padx=5
        )
        
        self.btn_procesar = ctk.CTkButton(
            self.buttons_frame,
            text="Procesar",
            command=self.procesar
        )

        self.btn_procesar.grid(
            row=0,
            column=2,
            padx=5
        )

    def crear_footer(self) -> None:

        self.footer_frame = ctk.CTkFrame(self.main_frame)

        self.footer_frame.grid(
            row=3,
            column=0,
            sticky="ew"
        )

        self.footer_frame.grid_columnconfigure(1, weight=1)

        self.lbl_estado_titulo = ctk.CTkLabel(
            self.footer_frame,
            text="Estado:"
        )

        self.lbl_estado_titulo.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        self.lbl_estado = ctk.CTkLabel(
            self.footer_frame,
            text="Esperando selección de archivo."
        )

        self.lbl_estado.grid(
            row=0,
            column=1,
            sticky="w"
        )

    # =====================================================
    # Eventos
    # =====================================================

    def seleccionar_archivo(self) -> None:

        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar CSV",
            filetypes=[
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not ruta_archivo:
            return

        self.ruta_archivo = ruta_archivo

        self.lbl_archivo.configure(
            text=Path(ruta_archivo).name
        )

        self.lbl_estado.configure(
            text="Leyendo columnas..."
        )

        try:
            columnas = obtener_columnas(ruta_archivo)
        except Exception as error:
            self.ruta_archivo = None
            self.lbl_archivo.configure(
                text="Ningún archivo seleccionado"
            )
            self.mostrar_columnas([])
            self.lbl_estado.configure(
                text=f"Error al leer el archivo: {error}"
            )
            return

        self.mostrar_columnas(columnas)

        self.lbl_estado.configure(
            text=f"{len(columnas)} columnas encontradas."
        )

    # =====================================================
    # Métodos auxiliares
    # =====================================================

    def mostrar_columnas(
        self,
        columnas: list[str]
    ) -> None:

        # Eliminar checkboxes anteriores
        for widget in self.checkboxes_frame.winfo_children():
            widget.destroy()

        self.columnas_disponibles.clear()

        # Crear un checkbox por columna
        for fila, columna in enumerate(columnas):

            checkbox_var = ctk.BooleanVar(value=True)

            checkbox = ctk.CTkCheckBox(
                self.checkboxes_frame,
                text=columna,
                variable=checkbox_var
            )

            checkbox.grid(
                row=fila,
                column=0,
                sticky="w",
                padx=10,
                pady=3
            )

            self.columnas_disponibles[columna] = checkbox_var

    def obtener_columnas_seleccionadas(self) -> list[str]:

        return [
            nombre
            for nombre, variable
            in self.columnas_disponibles.items()
            if variable.get()
        ]

    def seleccionar_todas(self) -> None:

        for variable in self.columnas_disponibles.values():
            variable.set(True)
        
    def deseleccionar_todas(self) -> None:

        for variable in self.columnas_disponibles.values():
            variable.set(False)
            
    def procesar(self) -> None:

        if self.ruta_archivo is None:
            self.lbl_estado.configure(
                text="Debe seleccionar un archivo CSV."
            )
            return

        columnas = self.obtener_columnas_seleccionadas()

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
            ruta_salida = procesar_csv(
                self.ruta_archivo,
                columnas
            )
        except Exception as error:
            self.lbl_estado.configure(
                text=f"Error al procesar: {error}"
            )
            return

        self.lbl_estado.configure(
            text=f"Archivo generado: {ruta_salida.name}"
        )