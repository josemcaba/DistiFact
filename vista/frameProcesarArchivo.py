"""
Módulo que contiene la clase FrameProcesamiento para mostrar el progreso del procesamiento.
"""
import tkinter as tk
from tkinter import ttk
import threading

from vista.frameBase import FrameBase

class ProcesarArchivo(FrameBase):
    def __init__(self, parent, app, controlador):
        self.titulo="Procesamiento de Facturas"
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

        separador1 = ttk.Separator(self._contenedor, orient="horizontal")
        separador1.grid(row=2, column=0, sticky="ew", columnspan=2, pady=5)
        
        etiqueta_archivo = ttk.Label(self._contenedor, text="Archivo a procesar:")
        etiqueta_archivo.grid(row=3, column=0, sticky="w", columnspan=2, padx=5, pady=5)

        self._valor_archivo = ttk.Label(self._contenedor, text="Ninguno", relief="solid", padding=5)
        self._valor_archivo.grid(row=4, column=0, sticky="w", columnspan=2, pady=(5, 10), padx=(30, 5))

        separador2 = ttk.Separator(self._contenedor, orient="horizontal")
        separador2.grid(row=5, column=0, sticky="ew", columnspan=2, pady=5)
        
        etiqueta_estado = ttk.Label(self._contenedor, text="Procesando 34 de 50")
        etiqueta_estado.grid(row=6, column=0, sticky="w", padx=5, pady=5)

        etiqueta_detalle = ttk.Label(self._contenedor, text="68% completado")
        etiqueta_detalle.grid(row=6, column=1, sticky="e", padx=5, pady=5)

        self.progreso = ttk.Progressbar(self._contenedor, orient="horizontal", mode="determinate")
        self.progreso.grid(row=7, column=0, sticky="ew", columnspan=2, padx=5, pady=5)
        self.progreso["value"] = 68

        self.txt_mensajes = tk.Text(self._contenedor, height=4, state='disabled')
        self.txt_mensajes.grid(row=8, column=0, sticky="nsew", columnspan=2, padx=5, pady=(5, 0))
    

    def inicializar(self):
        ''' 
        Procesos que no se pueden ejecutar durante la construccion
        del objeto por faltar información de la empresa
        '''
        # Rellena el campo con el nombre de la empresa y otros datos
        self._empresa = self.controlador.obtener_empresa_actual()
        self._valor_empresa.configure(text=self._empresa)

        self._archivo = self.controlador.obtener_ruta_archivo()
        if len(self._archivo) > 75:
            ruta_archivo = self._archivo[-75:]
            ruta_archivo = "..." + ruta_archivo[ruta_archivo.index("/"):]
        self._valor_archivo.configure(text=ruta_archivo)

    def _crear_botones(self):	# Marco para los botones
        marco_botones = ttk.Frame(self)
        marco_botones.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        # Botón para procesar la selección
        btn_procesar = ttk.Button(
            marco_botones,
            text="Continuar", 
            command=lambda: self.app.mostrar_frame('Resultados'), #self._on_continuar,
            # state='disabled'
        )
        btn_procesar.grid(row=0, column=0, padx=5)

        # Botón de salir
        self.btn_salir = ttk.Button(
            marco_botones, 
            text="Cancelar",
            command=lambda: self.app.mostrar_frame('SeleccionarArchivo')
        )
        self.btn_salir.grid(row=0, column=1)


    # def _obtener_titulo(self) -> str:
    #     """Retorna el título del frame."""
    #     return "Procesamiento de Facturas"
    
    # def _inicializar_componentes(self):
    #     """Inicializa los componentes del frame."""
    #     super()._inicializar_componentes()
        
    #     # Contenedor principal
    #     self.frame_contenido = ttk.Frame(self)
    #     self.frame_contenido.pack(fill="both", expand=True)
        
    #     # Información del archivo
    #     self.frame_info = ttk.Frame(self.frame_contenido)
    #     self.frame_info.pack(fill="x", pady=10)
        
    #     self.lbl_archivo_titulo = ttk.Label(
    #         self.frame_info,
    #         text="Archivo a procesar:",
    #         font=("Arial", 10, "bold")
    #     )
    #     self.lbl_archivo_titulo.pack(anchor="w")
        
    #     self.lbl_archivo_info = ttk.Label(
    #         self.frame_info,
    #         text="",
    #         padding=(20, 5)
    #     )
    #     self.lbl_archivo_info.pack(anchor="w")
        
    #     # Estado del procesamiento
    #     self.frame_estado = ttk.Frame(self.frame_contenido)
    #     self.frame_estado.pack(fill="x", pady=20)
        
    #     self.lbl_estado = ttk.Label(
    #         self.frame_estado,
    #         text="Preparando procesamiento...",
    #         padding=(0, 10)
    #     )
    #     self.lbl_estado.pack(anchor="w")
        
    #     # Barra de progreso
    #     self.progreso = ttk.Progressbar(
    #         self.frame_estado,
    #         orient="horizontal",
    #         length=500,
    #         mode="determinate"
    #     )
    #     self.progreso.pack(fill="x", pady=10)
        
    #     # Detalles del progreso
    #     self.lbl_detalle = ttk.Label(
    #         self.frame_estado,
    #         text="",
    #         padding=(0, 5)
    #     )
    #     self.lbl_detalle.pack(anchor="w")
        
    #     # Frame para mensajes
    #     self.frame_mensajes = ttk.Frame(self.frame_contenido)
    #     self.frame_mensajes.pack(fill="both", expand=True, pady=10)
        
    #     # Área de texto para mensajes
    #     self.txt_mensajes = tk.Text(
    #         self.frame_mensajes,
    #         height=10,
    #         width=70,
    #         wrap=tk.WORD,
    #         state=tk.DISABLED,
    #         font=("Consolas", 9)
    #     )
    #     self.txt_mensajes.pack(side="left", fill="both", expand=True)
        
    #     # Scrollbar para mensajes
    #     self.scrollbar = ttk.Scrollbar(
    #         self.frame_mensajes,
    #         command=self.txt_mensajes.yview
    #     )
    #     self.scrollbar.pack(side="right", fill="y")
    #     self.txt_mensajes.config(yscrollcommand=self.scrollbar.set)
        
    #     # Frame para botones
    #     self.frame_botones = ttk.Frame(self.frame_contenido)
    #     self.frame_botones.pack(fill="x", pady=10)
        
    #     # Botón de cancelar
    #     self.btn_cancelar = ttk.Button(
    #         self.frame_botones,
    #         text="Cancelar",
    #         command=self._on_cancelar
    #     )
    #     self.btn_cancelar.pack(side="right", padx=5)

    #     # Botón de continuar (inicialmente desactivado)
    #     self.btn_continuar = ttk.Button(
    #         self.frame_botones,
    #         text="Continuar",
    #         command=self._on_continuar,
    #         state="disabled"
    #     )
    #     self.btn_continuar.pack(side="right", padx=5)

        
    #     # Variable para controlar el hilo de procesamiento
    #     self.hilo_procesamiento = None
    #     self.cancelar_procesamiento = False
    
    # def inicializar(self):
    #     """Inicializa el frame cuando se muestra."""
    #     # 🔽 Aquí se desactiva el botón "Continuar" al iniciar
    #     self.btn_continuar.config(state="disabled")
        
    #     # Obtener información del archivo
    #     ruta_archivo = self.controlador.obtener_ruta_archivo()
        
    #     if not ruta_archivo:
    #         self.mostrar_mensaje("error", "No hay archivo seleccionado.")
    #         self.app.mostrar_frame("seleccion_archivo")
    #         return
        
    #     # Mostrar información del archivo
    #     if len(ruta_archivo) > 75:
    #         ruta_archivo = ruta_archivo[-75:]
    #         ruta_archivo = "..." + ruta_archivo[ruta_archivo.index("/"):]
    #     self.lbl_archivo_info.config(text=ruta_archivo)
        
    #     # Limpiar área de mensajes
    #     self.txt_mensajes.config(state=tk.NORMAL)
    #     self.txt_mensajes.delete(1.0, tk.END)
    #     self.txt_mensajes.config(state=tk.DISABLED)
        
    #     # Reiniciar barra de progreso
    #     self.progreso["value"] = 0
        
    #     # Reiniciar estado
    #     self.lbl_estado.config(text="Iniciando procesamiento...")
    #     self.lbl_detalle.config(text="")
        
    #     # Reiniciar variable de cancelación
    #     self.cancelar_procesamiento = False
        
    #     # Iniciar procesamiento en un hilo separado
    #     self.hilo_procesamiento = threading.Thread(
    #         target=self._procesar_archivo,
    #         daemon=True
    #     )
    #     self.hilo_procesamiento.start()
    
    # def _procesar_archivo(self):
    #     """Procesa el archivo en un hilo separado."""
    #     try:
    #         # Configurar callbacks para recibir actualizaciones
    #         self.controlador.configurar_callbacks(
    #             progreso_callback=self._actualizar_progreso,
    #             mensaje_callback=self._agregar_mensaje
    #         )
            
    #         # Iniciar procesamiento
    #         resultado = self.controlador.procesar_archivo()
            
    #         # Verificar si se canceló
    #         if self.cancelar_procesamiento:
    #             return
            
    #         # Verificar resultado
    #         if resultado:
    #             # Actualizar estado
    #             self._actualizar_estado("Procesamiento completado", 100)
                
    #             # Mostrar mensaje de éxito
    #             self._agregar_mensaje("info", f"Se procesaron {len(resultado)} facturas correctamente.")
                
    #             # Esperar antes de avanzar
    #             self.after(0, lambda: self.btn_continuar.config(state="normal"))

    #         else:
    #             # Actualizar estado
    #             self._actualizar_estado("Error en el procesamiento", 0)
                
    #             # Mostrar mensaje de error
    #             self._agregar_mensaje("error", "No se pudieron procesar facturas.")
            
    #         # ✅ Habilitar botón Continuar pase lo que pase
    #         self.after(0, lambda: self.btn_continuar.config(state="normal"))
        
    #     except Exception as e:
    #         # Mostrar error
    #         self._actualizar_estado(f"Error: {str(e)}", 0)
    #         self._agregar_mensaje("error", f"Error durante el procesamiento: {str(e)}")
    #         self.after(0, lambda: self.btn_continuar.config(state="normal"))  # ✅ También en errores críticos
    
    # def _actualizar_progreso(self, actual, total):
    #     """
    #     Actualiza la barra de progreso.
        
    #     Args:
    #         actual: Valor actual del progreso
    #         total: Valor total del progreso
    #     """
    #     # Calcular porcentaje
    #     if total > 0:
    #         porcentaje = int((actual / total) * 100)
    #     else:
    #         porcentaje = 0
        
    #     # Actualizar en el hilo principal
    #     self.after(0, lambda: self._actualizar_estado(
    #         f"Procesando {actual} de {total}",
    #         porcentaje
    #     ))
    
    # def _actualizar_estado(self, texto, porcentaje):
    #     """
    #     Actualiza el estado y la barra de progreso.
        
    #     Args:
    #         texto: Texto de estado
    #         porcentaje: Porcentaje de progreso (0-100)
    #     """
    #     self.lbl_estado.config(text=texto)
    #     self.progreso["value"] = porcentaje
    #     self.lbl_detalle.config(text=f"{porcentaje}% completado")
    
    # def _agregar_mensaje(self, tipo, mensaje):
    #     """
    #     Agrega un mensaje al área de texto.
        
    #     Args:
    #         tipo: Tipo de mensaje ('info', 'error', 'warning')
    #         mensaje: Contenido del mensaje
    #     """
    #     # Prefijo según tipo
    #     if tipo == "error":
    #         prefijo = "❌ ERROR: "
    #     elif tipo == "warning":
    #         prefijo = "⚠️ AVISO: "
    #     else:
    #         prefijo = "INFO: "
        
    #     # Agregar mensaje en el hilo principal
    #     self.after(0, lambda: self._insertar_mensaje(f"{prefijo}{mensaje}\n"))
    
    # def _insertar_mensaje(self, texto):
    #     """
    #     Inserta un mensaje en el área de texto.
        
    #     Args:
    #         texto: Texto a insertar
    #     """
    #     self.txt_mensajes.config(state=tk.NORMAL)
    #     self.txt_mensajes.insert(tk.END, texto)
    #     self.txt_mensajes.see(tk.END)  # Desplazar al final
    #     self.txt_mensajes.config(state=tk.DISABLED)
    
    # def _on_cancelar(self):
    #     """Maneja el evento de cancelar procesamiento."""
    #     if self.hilo_procesamiento and self.hilo_procesamiento.is_alive():
    #         # Marcar como cancelado
    #         self.cancelar_procesamiento = True
            
    #         # Actualizar estado
    #         self._actualizar_estado("Cancelando procesamiento...", 0)
            
    #         # Volver al frame anterior
    #         self.after(1000, lambda: self.app.mostrar_frame("seleccion_archivo"))
    #     else:
    #         # Si no hay procesamiento activo, volver directamente
    #         self.app.mostrar_frame("seleccion_archivo")

    # def _on_continuar(self):
    #     """Maneja el evento de continuar tras procesamiento."""
    #     self.app.mostrar_frame("resultados")

