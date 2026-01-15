import tkinter as tk
from tkinter import ttk
import os
from vista.frame_base import FrameBase

class FrameSeleccionArchivo(FrameBase):
    nombre = "seleccion_archivo"
    
    def _obtener_titulo(self) -> str:
        return "Selección de Archivo"
    
    def _inicializar_componentes(self):
        super()._inicializar_componentes()
        
        # Crear cabecera con información de empresa y botón Unificar
        self._crear_cabecera_empresa(mostrar_boton=True)
        
        # Frame principal que contendrá todo el contenido
        self.frame_principal = ttk.Frame(self)
        self.frame_principal.pack(fill="both", expand=True)
        
        # Frame para el contenido que debe expandirse (arriba)
        self.frame_contenido = ttk.Frame(self.frame_principal)
        self.frame_contenido.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Frame fijo para botones de navegación (abajo)
        self.frame_botones_inferiores = ttk.Frame(self.frame_principal)
        self.frame_botones_inferiores.pack(side="bottom", fill="x", padx=5)
        
        self._crear_area_seleccion_archivo()
        self._crear_area_acciones()
    
    def _crear_area_seleccion_archivo(self):
        frame = ttk.Frame(self.frame_contenido)
        frame.pack(fill="x", pady=5)
        
        ttk.Label(frame, text="Archivo a procesar:").pack(anchor="w", pady=(0, 5))
        
        f_entrada = ttk.Frame(frame)
        f_entrada.pack(fill="x", pady=5)
        ttk.Button(f_entrada, text="Examinar", command=self._on_examinar).pack(side="left")
        self.entry_ruta = ttk.Entry(f_entrada)
        self.entry_ruta.pack(side="right", fill="x", expand=True, padx=(10, 0))

    def _crear_area_acciones(self):
        # Botones de navegación en el frame inferior (siempre pegados abajo)
        f_nav = ttk.Frame(self.frame_botones_inferiores)
        f_nav.pack(fill="x")
        
        ttk.Button(f_nav, text="Procesar", command=self._on_procesar).pack(side="right")
        ttk.Button(f_nav, text="Volver", command=lambda: self.app.mostrar_frame("seleccion_empresa")).pack(side="right", padx=5)

        self.btn_crear = ttk.Button(f_nav, text="Crear rectángulos", width=17, command=self._on_crear_rectangulos)
        self.btn_visualizar = ttk.Button(f_nav, text="Ver rectángulos", width=17, command=self._on_visualizar_rectangulos)
        
        # Inicialmente no los empaquetamos
        self.btn_crear.pack_forget()
        self.btn_visualizar.pack_forget()

    def inicializar(self):
        # Actualizar información de empresa en la cabecera
        self._actualizar_info_empresa()
        
        empresa = self.controlador.obtener_empresa_actual()
        if not empresa:
            self.app.mostrar_frame("seleccion_empresa")
            return
            
        self.entry_ruta.delete(0, tk.END)
        self._actualizar_visibilidad_botones(empresa.tipo)
    
    def _actualizar_visibilidad_botones(self, tipo_empresa):
        if tipo_empresa == "PDFimagen":
            self.btn_visualizar.pack(side="left")
            self.btn_crear.pack(side="left", padx=5)
        else:
            self.btn_visualizar.pack_forget()
            self.btn_crear.pack_forget()

    def _validar_archivo(self, ruta, extensiones):
        if not ruta or not os.path.isfile(ruta):
            return False, "El archivo no existe."
        if not ruta.lower().endswith(extensiones):
            return False, f"Extensión inválida. Se espera: {extensiones}"
        return True, ""

    def _on_examinar(self):
        empresa = self.controlador.obtener_empresa_actual()
        ext = "*.xlsx;*.xls" if empresa.tipo == "excel" else "*.pdf"
        ruta = self.app.seleccionar_archivo([("Archivos", ext)], f"Seleccionar para {empresa.nombre}")
        if ruta:
            self.entry_ruta.delete(0, tk.END)
            self.entry_ruta.insert(0, ruta)

    def _on_procesar(self):
        ruta = self.entry_ruta.get().strip()
        empresa = self.controlador.obtener_empresa_actual()
        
        exts = (".xlsx", ".xls") if empresa.tipo == "excel" else (".pdf",)
        valido, msg = self._validar_archivo(ruta, exts)
        
        if not valido:
            self.mostrar_mensaje("error", msg)
            return
            
        self.controlador.establecer_ruta_archivo(ruta)
        self.app.mostrar_frame("procesamiento")
    
    def _on_visualizar_rectangulos(self):
        ruta = self.entry_ruta.get().strip()
        valido, msg = self._validar_archivo(ruta, (".pdf",))
        if valido:
            self.controlador.visualizar_rectangulos(ruta, self.controlador.obtener_empresa_actual().to_dict())
        else:
             self.mostrar_mensaje("error", msg)

    def _on_crear_rectangulos(self):
        ruta = self.entry_ruta.get().strip()
        valido, msg = self._validar_archivo(ruta, (".pdf",))
        if valido:
             self.controlador.crear_rectangulos(ruta, self.controlador.obtener_empresa_actual().to_dict())
        else:
             self.mostrar_mensaje("error", msg)

    def _on_unificar_pdfs(self):
        directorio = self.app.seleccionar_directorio("Directorio con PDFs a unificar")
        if directorio:
            res = self.controlador.unificar_pdfs(directorio)
            tipo = "info" if res["exito"] else "error"
            self.mostrar_mensaje(tipo, res["mensaje"] + (f"\nGenerado: {res.get('ruta_salida')}" if res.get('ruta_salida') else ""))
            