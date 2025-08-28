import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror, showwarning
import os

from vista.frameBase import FrameBase

class SeleccionarArchivo(FrameBase):
    def __init__(self, parent, app, controlador):
        self.titulo="Selección de Archivo"
        super().__init__(parent, app, controlador, self.titulo)
        self._configurar_marco()
        self._crear_botones()
    
    def _configurar_marco(self):
        self._contenedor = ttk.Frame(self)
        self._contenedor.columnconfigure(0, weight=0)  # Columna de etiquetas y botón
        self._contenedor.columnconfigure(1, weight=1)  # Columna de valores y entrada
        self._contenedor.grid(sticky="nsew", padx=5)

        etiqueta_empresa = ttk.Label(self._contenedor, text="Empresa seleccionada:")
        etiqueta_empresa.grid(row=0, column=0, sticky="w", columnspan=2, padx=5, pady=5)

        self._valor_empresa = ttk.Label(self._contenedor, text="Ninguna", relief="solid", padding=5)
        self._valor_empresa.grid(row=1, column=0, sticky="w", columnspan=2, pady=(5, 10), padx=(30, 5))
        
        separador = ttk.Separator(self._contenedor, orient="horizontal")
        separador.grid(row=2, column=0, sticky="ew", columnspan=2, pady=5)
        
        etiqueta_archivo = ttk.Label(self._contenedor, text="Archivo a procesar:")
        etiqueta_archivo.grid(row=3, column=0, sticky="w", columnspan=2, padx=5, pady=5)
        
        btn_examinar = ttk.Button(self._contenedor, text="Examinar", command=self._on_examinar)
        btn_examinar.grid(row=4, column=0, sticky='w', padx=(10, 5), pady=5)
        
        self.entry_ruta = ttk.Entry(self._contenedor, font=('Arial', 10))
        self.entry_ruta.grid(row=4, column=1, sticky="nsew", padx=5, pady=10)

    def inicializar(self):
        ''' 
        Procesos que no se pueden ejecutar durante la construccion
        del objeto por faltar información de la empresa
        '''
        # Rellena el campo con el nombre de la empresa y otros datos
        self._empresa = self.controlador.obtener_empresa_actual()
        self._valor_empresa.configure(text=self._empresa)

        # Limpiar campo de ruta
        self.entry_ruta.delete(0, tk.END)

        # Botones sobre rectanguls que se mostrarán solo si es PDF imagen
        if self._empresa.tipo=='PDFimagen':
            self.btn_crear.grid(row=0, column=0, sticky='w')
            self.btn_visualizar.grid(row=0, column=1, sticky='w', padx=5)
        else:
            self.btn_crear.grid_forget()
            self.btn_visualizar.grid_forget()


    def _crear_botones(self):
        marco_botones = ttk.Frame(self)
        marco_botones.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        marco_botones.columnconfigure(0, weight=0)
        marco_botones.columnconfigure(1, weight=0)
        marco_botones.columnconfigure(2, weight=1)
        marco_botones.columnconfigure(3, weight=0)
        marco_botones.columnconfigure(4, weight=0)

        # Botón para crear rectángulos (solo visible para PDF imagen)
        self.btn_crear = ttk.Button(
            marco_botones,
            text="Crear Rectángulos",
            width=22,
            command=self._on_crear_rectangulos
        )
        # No se empaqueta aquí, se mostrará solo si es PDF imagen
        
        # Botón para visualizar rectángulos (solo visible para PDF imagen)
        self.btn_visualizar = ttk.Button(
            marco_botones,
            text="Visualizar Rectángulos",
            width=22,
            command=self._on_visualizar_rectangulos
        )
        # No se empaqueta aquí, se mostrará solo si es PDF imagen


        btn_procesar = ttk.Button(
            marco_botones, 
            text="Procesar", 
            command=self._on_procesar,
			# state='disabled'
        )
        btn_procesar.grid(row=0, column=3, sticky='e', padx=5)

        self.btn_salir = ttk.Button(
            marco_botones, 
            text="Volver atrás",
            command=lambda: self.app.mostrar_frame("SeleccionarEmpresa")
        )
        self.btn_salir.grid(row=0, column=4, sticky='e')
    
    def _on_examinar(self):
        if self._empresa.tipo == "excel":
            tipos_archivo = [("Archivos Excel", "*.xlsx;*.xls")]
        else:
            tipos_archivo = [("Archivos PDF", "*.pdf")]

        # Mostrar diálogo de selección
        ruta = filedialog.askopenfilename(
            title=f"Seleccionar archivo para {self._empresa.nombre}",
            filetypes=tipos_archivo
        )
        if ruta:
            self.entry_ruta.delete(0, tk.END)
            self.entry_ruta.insert(0, ruta)
            # self._btn_procesar.config(state="normal")

    def _on_procesar(self):
        """Maneja el evento de procesar archivo."""
        # Obtener ruta del archivo
        ruta = self.entry_ruta.get().strip()
        
        if not ruta:
            showwarning("Atención", "Debe seleccionar un archivo.")
            return
        
        if not os.path.isfile(ruta):
            showerror("Error", f"El archivo '{ruta}' no existe.")
            return
        
        if self._empresa.tipo in ["PDFtexto", "PDFimagen"] and not ruta.lower().endswith(".pdf"):
            showerror("Error", "El archivo debe ser un PDF.")
            return
        
        if self._empresa.tipo == "excel" and not ruta.lower().endswith((".xlsx", ".xls")):
            showerror("Error", "El archivo debe ser un Excel.")
            return
        
        # Establecer ruta en el controlador
        self.controlador.establecer_ruta_archivo(ruta)
        
        # Avanzar al frame de procesamiento
        self.app.mostrar_frame("ProcesarArchivo")
  
    
    def _on_visualizar_rectangulos(self):
        """Maneja el evento de visualizar rectángulos."""
        # Obtener ruta del archivo
        ruta = self.entry_ruta.get().strip()
        
        if not ruta:
            showwarning("Atención", "Debe seleccionar un archivo.")
            return
        
        if not os.path.isfile(ruta):
            showerror("Error", f"El archivo '{ruta}' no existe.")
            return
        
        if not ruta.lower().endswith(".pdf"):
            showerror("Error", "El archivo debe ser un PDF.")
            return
        
        # Visualizar rectángulos
        self.controlador.visualizar_rectangulos(ruta, self._empresa.to_dict())

    def _on_crear_rectangulos(self):
        """Maneja el evento de crear rectángulos."""
        ruta = self.entry_ruta.get().strip()
    
        if not ruta:
            showwarning("Atención", "Debe seleccionar un archivo.")
            return
        
        if not os.path.isfile(ruta):
            showerror("Error", f"El archivo '{ruta}' no existe.")
            return
        
        if not ruta.lower().endswith(".pdf"):
            showerror("Error", "El archivo debe ser un PDF.")
            return
    
        # Llamar al controlador para crear los rectángulos
        self.controlador.crear_rectangulos(ruta, self._empresa.to_dict())

        

