import tkinter as tk
from tkinter import ttk
import threading
from vista.frame_base import FrameBase

class FrameProcesamiento(FrameBase):
    nombre = "procesamiento"
    
    def _obtener_titulo(self) -> str:
        return "Procesamiento de Facturas"
    
    def _inicializar_componentes(self):
        super()._inicializar_componentes()
        
        self.frame_contenido = ttk.Frame(self)
        self.frame_contenido.pack(fill="both", expand=True)
        
        # Info Archivo
        self.lbl_archivo_info = ttk.Label(self.frame_contenido, text="", padding=(20, 10))
        self.lbl_archivo_info.pack(anchor="w")
        
        # Estado y Progreso
        f_estado = ttk.Frame(self.frame_contenido)
        f_estado.pack(fill="x", pady=10)
        
        self.lbl_estado = ttk.Label(f_estado, text="Preparando...")
        self.lbl_estado.pack(anchor="w")
        
        self.progreso = ttk.Progressbar(f_estado, orient="horizontal", length=500, mode="determinate")
        self.progreso.pack(fill="x", pady=5)
        
        self.lbl_detalle = ttk.Label(f_estado, text="")
        self.lbl_detalle.pack(anchor="w")
        
        # Log de mensajes
        f_msgs = ttk.Frame(self.frame_contenido)
        f_msgs.pack(fill="both", expand=True, pady=10)
        
        self.txt_mensajes = tk.Text(f_msgs, height=10, state=tk.DISABLED, font=("Consolas", 9))
        self.txt_mensajes.pack(side="left", fill="both", expand=True)
        
        scroll = ttk.Scrollbar(f_msgs, command=self.txt_mensajes.yview)
        scroll.pack(side="right", fill="y")
        self.txt_mensajes.config(yscrollcommand=scroll.set)
        
        # Botones
        f_btns = ttk.Frame(self.frame_contenido)
        f_btns.pack(fill="x", pady=10)
        
        self.btn_continuar = ttk.Button(f_btns, text="Continuar", command=lambda: self.app.mostrar_frame("resultados"), state="disabled")
        self.btn_continuar.pack(side="right", padx=5)
        
        self.btn_cancelar = ttk.Button(f_btns, text="Cancelar", command=self._on_cancelar)
        self.btn_cancelar.pack(side="right", padx=5)
        
        self.cancelar_procesamiento = False

    def inicializar(self):
        self.btn_continuar.config(state="disabled")
        ruta = self.controlador.obtener_ruta_archivo()
        
        if not ruta:
            self.app.mostrar_frame("seleccion_archivo")
            return
            
        ruta_display = "..." + ruta[-70:] if len(ruta) > 75 else ruta
        self.lbl_archivo_info.config(text=f"Procesando: {ruta_display}")
        
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
            self.controlador.configurar_callbacks(
                progreso_callback=self._actualizar_progreso,
                mensaje_callback=self._agregar_mensaje
            )
            
            res = self.controlador.procesar_archivo()
            
            if self.cancelar_procesamiento: return
            
            if res:
                self._actualizar_estado("Completado", 100)
                self._agregar_mensaje("info", f"Generadaos {len(res)} apuntes")
            else:
                self._actualizar_estado("Error", 0)
                self._agregar_mensaje("error", "No se procesaron facturas.")
                
        except Exception as e:
            self._actualizar_estado(f"Error crítico", 0)
            self._agregar_mensaje("error", str(e))
        finally:
            self.after(0, lambda: self.btn_continuar.config(state="normal"))

    def _actualizar_progreso(self, actual, total):
        pct = int((actual / total) * 100) if total > 0 else 0
        self.after(0, lambda: self._actualizar_estado(f"Procesando {actual}/{total}", pct))

    def _actualizar_estado(self, texto, porcentaje):
        self.lbl_estado.config(text=texto)
        self.progreso["value"] = porcentaje
        self.lbl_detalle.config(text=f"{porcentaje}%")

    def _agregar_mensaje(self, tipo, mensaje):
        iconos = {"error": "❌ ", "warning": "⚠️ ", "info": "ℹ️ "}
        texto = f"{iconos.get(tipo, '')}{mensaje}\n"
        
        def _write():
            self.txt_mensajes.config(state=tk.NORMAL)
            self.txt_mensajes.insert(tk.END, texto)
            self.txt_mensajes.see(tk.END)
            self.txt_mensajes.config(state=tk.DISABLED)
            
        self.after(0, _write)

    def _on_cancelar(self):
        self.cancelar_procesamiento = True
        self._agregar_mensaje("warning", "Cancelando...")
        self.after(1000, lambda: self.app.mostrar_frame("seleccion_archivo"))