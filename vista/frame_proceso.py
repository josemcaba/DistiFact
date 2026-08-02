import tkinter as tk
from tkinter import ttk
import threading
from vista.frame_base import FrameBase
import extractores.conceptos_factura as KEY

class FrameProcesamiento(FrameBase):
    nombre = "procesamiento"
    
    def _obtener_titulo(self) -> str:
        return "Procesamiento de Facturas"
    
    def _inicializar_componentes(self):
        super()._inicializar_componentes()
        
        # Crear cabecera con información de empresa (sin botón)
        self._crear_cabecera_empresa(mostrar_boton=False)

        # Crear sub-cabecera con información del archivo a procesar
        self._crear_cabecera_archivo()
        
        # Frame principal que contendrá todo el contenido
        self.frame_principal = ttk.Frame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=5, pady=(5, 0))
        
        # Estado y Barra de Progreso
        f_estado = ttk.Frame(self.frame_principal)
        f_estado.pack(fill="x")
        
        # Frame para los labels
        f_labels = ttk.Frame(f_estado)
        f_labels.pack(fill="x", side="top")

        self.lbl_estado = ttk.Label(f_labels, text="Preparando...")
        self.lbl_estado.pack(side="left")
        
        self.lbl_detalle = ttk.Label(f_labels, text="")
        self.lbl_detalle.pack(side="right")

        self.progreso = ttk.Progressbar(f_estado, orient="horizontal", mode="determinate")
        self.progreso.pack(fill="x", pady=(5, 0))
        
        
        # Log de mensajes
        f_msgs = ttk.Frame(self.frame_principal)
        f_msgs.pack(fill="both", expand=True, pady=(10, 5))
        
        self.txt_mensajes = tk.Text(f_msgs, height=0, width=0, state=tk.DISABLED, font=("Consolas", 9))
        self.txt_mensajes.pack(side="left", fill="both", expand=True)
        
        scroll = ttk.Scrollbar(f_msgs, command=self.txt_mensajes.yview)
        scroll.pack(side="right", fill="y")
        self.txt_mensajes.config(yscrollcommand=scroll.set)
        
        self._crear_area_botones()

        self.cancelar_procesamiento = False

    def _crear_area_botones(self):
        # Botones de navegación en el frame inferior (siempre pegados abajo)
        f_botones = ttk.Frame(self.frame_principal)
        f_botones.pack(side="bottom", fill="x")

        self.boton_continuar = ttk.Button(f_botones, text="Continuar", command=lambda: self.app.mostrar_frame("resultados"), state="disabled")
        self.boton_continuar.pack(side="left")

        self.boton_cancelar = ttk.Button(f_botones, text="Cancelar", command=self._on_cancelar)
        self.boton_cancelar.pack(side="left", padx=5)
   

    def _crear_cabecera_archivo(self):
        """Crea la cabecera con información de la empresa seleccionada."""
        # Frame para información de archivo
        self.frame_archivo = ttk.Frame(self)
        self.frame_archivo.pack(fill="x", padx=5, pady=5)
        
        # Información del archivo (izquierda)
        f_info_archivo = ttk.Frame(self.frame_archivo)
        f_info_archivo.pack(side="left", fill="x", expand=True)
        
        ttk.Label(f_info_archivo, text="Archivo:").pack(anchor="w")
        self.lbl_archivo = ttk.Label(f_info_archivo,
            relief="solid", padding=5, text="", 
            style="Info.TLabel")  # Nuevo estilo para información de empresa
        
        self.lbl_archivo.pack(anchor="w", pady=(5, 0), padx=(0, 5))

        # Separador
        ttk.Separator(self, orient="horizontal").pack(fill='x', padx=5, pady=5)
    
    def _actualizar_info_archivo(self):
        """Actualiza la información del archivo en la cabecera."""
        ruta_archivo = self.controlador.obtener_ruta_archivo()
        if not ruta_archivo:
            self.lbl_archivo.config(text="")
            return
        if len(ruta_archivo) > 75:
            ruta_archivo = ruta_archivo[-75:]
            ruta_archivo = "..." + ruta_archivo[ruta_archivo.index("/"):]
        self.lbl_archivo.config(text=ruta_archivo)

    def inicializar(self):
        self.boton_continuar.config(state="disabled")

        # Actualizar información en la cabecera
        self._actualizar_info_empresa()
        self._actualizar_info_archivo()
        
        self._limpiar_log()
        self.progreso["value"] = 0
        self.cancelar_procesamiento = False
        
        threading.Thread(target=self._procesar_archivo, daemon=True).start()

    def _limpiar_log(self):
        self.txt_mensajes.config(state=tk.NORMAL)
        self.txt_mensajes.delete(1.0, tk.END)
        self.txt_mensajes.config(state=tk.DISABLED)

    def _procesar_archivo(self):
        try:
            # Configurar callbacks incluyendo el de factura
            self.controlador.configurar_callbacks(
                progreso_callback=self._actualizar_progreso,
                mensaje_callback=self._agregar_mensaje,
                factura_callback=self._agregar_info_factura
            )
            
            res = self.controlador.procesar_archivo()
            
            if self.cancelar_procesamiento: return
            
            if res:
                self._agregar_mensaje("info", f"Generados {len(res)} apuntes")
            else:
                self._actualizar_estado("Error", 0)
                self._agregar_mensaje("error", "No se procesaron facturas.")
                
        except Exception as e:
            self._actualizar_estado(f"Error crítico", 0)
            self._agregar_mensaje("error", str(e))
        finally:
            self.after(0, lambda: self.boton_continuar.config(state="normal"))

    def _actualizar_progreso(self, actual, total):
        pct = int((actual / total) * 100) if total > 0 else 0
        self.after(0, lambda: self._actualizar_estado(f"Procesando {actual} de {total}", pct))

    def _actualizar_estado(self, texto, porcentaje):
        self.lbl_estado.config(text=texto)
        self.progreso["value"] = porcentaje
        self.lbl_detalle.config(text=f"{porcentaje}% completado")

    def _agregar_mensaje(self, tipo, mensaje):
        iconos = {"error": "❌ ", "warning": "⚠️ ", "info": "ℹ️ "}
        texto = f"{iconos.get(tipo, '')}{mensaje}\n"
        
        def _write():
            self.txt_mensajes.config(state=tk.NORMAL)
            self.txt_mensajes.insert(tk.END, texto)
            self.txt_mensajes.see(tk.END)
            self.txt_mensajes.config(state=tk.DISABLED)
            
        self.after(0, _write)
    
    def _agregar_info_factura(self, factura: dict):
        """
        Agrega información de una factura procesada al log
        """
        icono = "📄 "
        texto = f"{icono}Factura: {factura[KEY.NUM_FACT]} {factura[KEY.FECHA_FACT]} {factura[KEY.BASE_IVA]} {factura[KEY.CUOTA_IVA]} {factura[KEY.TOTAL_FACT]}\n"
        
        def _write():
            self.txt_mensajes.config(state=tk.NORMAL)
            self.txt_mensajes.insert(tk.END, texto)
            self.txt_mensajes.see(tk.END)
            self.txt_mensajes.config(state=tk.DISABLED)
            
        self.after(0, _write)

    def _on_cancelar(self):
        self._agregar_mensaje("warning", "Cancelando...")
        self.after(1000, lambda: self.app.mostrar_frame("seleccion_archivo"))
        self.cancelar_procesamiento = True