import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror, showwarning
import os
from typing import Dict, Any, Optional

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
        btn_examinar.grid(row=4, column=0, sticky='w', padx=5, pady=5)
        
        self.entry_ruta = ttk.Entry(self._contenedor, font=('Arial', 10))
        self.entry_ruta.grid(row=4, column=1, sticky="nsew", padx=5, pady=10)

    def inicializar(self):
        ''' 
        Procesos que no se pueden ejecutar durante la creación del 
        objeto por faltar información de la empresa
        '''
        self._empresa = self.controlador.obtener_empresa_actual()
        self._valor_empresa.configure(text=self._empresa)

        # Limpiar campo de ruta
        self.entry_ruta.delete(0, tk.END)

    def _crear_botones(self):
        marco_botones = ttk.Frame(self)
        marco_botones.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        btn_procesar = ttk.Button(
            marco_botones, 
            text="Procesar", 
            command=self._on_procesar,
			# state='disabled'
        )
        btn_procesar.grid(row=0, column=0, padx=5)
        self._btn_procesar=btn_procesar

        self.btn_salir = ttk.Button(
            marco_botones, 
            text="Volver atrás",
            command=lambda: self.app.mostrar_frame("SeleccionarEmpresa")
        )
        self.btn_salir.grid(row=0, column=1)
    
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
        
        # Verificar extensión según tipo de empresa
        #empresa = self.controlador.obtener_empresa_actual()
        
        if self._empresa.tipo in ["PDFtexto", "PDFimagen"] and not ruta.lower().endswith(".pdf"):
            showerror("Error", "El archivo debe ser un PDF.")
            return
        
        if self._empresa.tipo == "excel" and not ruta.lower().endswith((".xlsx", ".xls")):
            showerror("Error", "El archivo debe ser un Excel.")
            return
        
        # Establecer ruta en el controlador
        self.controlador.establecer_ruta_archivo(ruta)
        
        # Avanzar al frame de procesamiento
        self.app.mostrar_frame("SeleccionarEmpresa")

 
    #     # Frame para botones
    #     self.frame_botones = ttk.Frame(self.frame_contenido)
    #     self.frame_botones.pack(fill="x", pady=20)

    #     # Botón para crear rectángulos (solo visible para PDF imagen)
    #     self.btn_crear = ttk.Button(
    #         self.frame_botones,
    #         text="Crear Rectángulos",
    #         command=self._on_crear_rectangulos
    #     )
    #     # No se empaqueta aquí, se mostrará solo si es PDF imagen
        
    #     # Botón para visualizar rectángulos (solo visible para PDF imagen)
    #     self.btn_visualizar = ttk.Button(
    #         self.frame_botones,
    #         text="Visualizar Rectángulos",
    #         command=self._on_visualizar_rectangulos
    #     )
    #     # No se empaqueta aquí, se mostrará solo si es PDF imagen

    #     # Botón de procesar
    #     self.btn_procesar = ttk.Button(
    #         self.frame_botones,
    #         text="Procesar",
    #         command=self._on_procesar
    #     )
    #     self.btn_procesar.pack(side="right", padx=5)
        
    #     # Botón de volver
    #     self.btn_volver = ttk.Button(
    #         self.frame_botones,
    #         text="Volver",
    #         command=lambda: self.app.mostrar_frame("seleccion_empresa")
    #     )
    #     self.btn_volver.pack(side="right", padx=5)
    
    # def inicializar(self):
    #     """Inicializa el frame cuando se muestra."""
    #     # Obtener información de la empresa seleccionada
    #     empresa = self.controlador.obtener_empresa_actual()
        
    #     if not empresa:
    #         self.mostrar_mensaje("error", "No hay empresa seleccionada.")
    #         self.app.mostrar_frame("seleccion_empresa")
    #         return
        
    #     # Mostrar información de la empresa
    #     self.lbl_empresa_info.config(
    #         text=f"{empresa.nombre} ({empresa.nif}) - Tipo: {empresa.tipo}"
    #     )
        
    #     # Mostrar u ocultar botón de visualizar rectángulos según tipo de empresa
    #     if empresa.tipo == "PDFimagen":
    #         self.btn_visualizar.pack(side="left", padx=5)
    #         self.btn_crear.pack(side="left", padx=5)
    #     else:
    #         self.btn_visualizar.pack_forget()
    #         self.btn_crear.pack_forget()
        
    #     # Limpiar campo de ruta
    #     self.entry_ruta.delete(0, tk.END)
    
    # def _on_examinar(self):
    #     """Maneja el evento de examinar archivo."""
    #     empresa = self.controlador.obtener_empresa_actual()
        
    #     if not empresa:
    #         return
        
    #     # Determinar tipo de archivo según el tipo de empresa
    #     if empresa.tipo == "excel":
    #         tipos_archivo = [("Archivos Excel", "*.xlsx;*.xls")]
    #     else:
    #         tipos_archivo = [("Archivos PDF", "*.pdf")]
        
    #     # Mostrar diálogo de selección
    #     ruta = self.app.seleccionar_archivo(
    #         tipos_archivo=tipos_archivo,
    #         titulo=f"Seleccionar archivo para {empresa.nombre}"
    #     )
        
    #     if ruta:
    #         self.entry_ruta.delete(0, tk.END)
    #         self.entry_ruta.insert(0, ruta)
    
    # def _on_visualizar_rectangulos(self):
    #     """Maneja el evento de visualizar rectángulos."""
    #     # Obtener ruta del archivo
    #     ruta = self.entry_ruta.get().strip()
        
    #     if not ruta:
    #         self.mostrar_mensaje("warning", "Debe seleccionar un archivo PDF.")
    #         return
        
    #     if not os.path.isfile(ruta):
    #         self.mostrar_mensaje("error", f"El archivo '{ruta}' no existe.")
    #         return
        
    #     if not ruta.lower().endswith(".pdf"):
    #         self.mostrar_mensaje("error", "El archivo debe ser un PDF.")
    #         return
        
    #     # Obtener empresa actual
    #     empresa = self.controlador.obtener_empresa_actual()

    #     # Visualizar rectángulos
    #     self.controlador.visualizar_rectangulos(ruta, empresa.to_dict())

    # def _on_crear_rectangulos(self):
    #     """Maneja el evento de crear rectángulos."""
    #     ruta = self.entry_ruta.get().strip()
    
    #     if not ruta:
    #         self.mostrar_mensaje("warning", "Debe seleccionar un archivo PDF.")
    #         return
    
    #     if not os.path.isfile(ruta):
    #         self.mostrar_mensaje("error", f"El archivo '{ruta}' no existe.")
    #         return
    
    #     if not ruta.lower().endswith(".pdf"):
    #         self.mostrar_mensaje("error", "El archivo debe ser un PDF.")
    #         return
    
    #     empresa = self.controlador.obtener_empresa_actual()
    
    #     # Llamar al controlador para crear los rectángulos
    #     self.controlador.crear_rectangulos(ruta, empresa.to_dict())

        
    # def _on_procesar(self):
    #     """Maneja el evento de procesar archivo."""
    #     # Obtener ruta del archivo
    #     ruta = self.entry_ruta.get().strip()
        
    #     if not ruta:
    #         self.mostrar_mensaje("warning", "Debe seleccionar un archivo.")
    #         return
        
    #     if not os.path.isfile(ruta):
    #         self.mostrar_mensaje("error", f"El archivo '{ruta}' no existe.")
    #         return
        
    #     # Verificar extensión según tipo de empresa
    #     empresa = self.controlador.obtener_empresa_actual()
        
    #     if empresa.tipo in ["PDFtexto", "PDFimagen"] and not ruta.lower().endswith(".pdf"):
    #         self.mostrar_mensaje("error", "El archivo debe ser un PDF.")
    #         return
        
    #     if empresa.tipo == "excel" and not ruta.lower().endswith((".xlsx", ".xls")):
    #         self.mostrar_mensaje("error", "El archivo debe ser un Excel.")
    #         return
        
    #     # Establecer ruta en el controlador
    #     self.controlador.establecer_ruta_archivo(ruta)
        
    #     # Avanzar al frame de procesamiento
    #     self.app.mostrar_frame("procesamiento")
