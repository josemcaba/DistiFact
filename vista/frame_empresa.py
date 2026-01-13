import tkinter as tk
from tkinter import ttk
from vista.frame_base import FrameBase
from vista.Tabla import Tabla 

class FrameSeleccionEmpresa(FrameBase):
    nombre = "seleccion_empresa"
    
    def _obtener_titulo(self) -> str:
        return "Selección de Empresa"
    
    def _inicializar_componentes(self):
        super()._inicializar_componentes()
        
        self.frame_contenido = ttk.Frame(self)
        self.frame_contenido.pack(fill="both", expand=True)
         
        # Tabla
        self.frame_tabla = ttk.Frame(self.frame_contenido)
        self.frame_tabla.pack(fill="both", expand=True, pady=5)
        
        self.tabla_empresas = Tabla(self.frame_tabla)
        self.tabla_empresas.pack(fill="both", expand=True)
        
        columnas = [
            {"nombre": "Num.", "ancho": 50, "alineacion": tk.CENTER, "expandible": False},
            {"nombre": "DNI/NIF", "ancho": 125, "alineacion": tk.CENTER, "expandible": False},
            {"nombre": "Razón Social", "ancho": 150, "alineacion": tk.W, "expandible": True},
            {"nombre": "Tipo", "ancho": 100, "alineacion": tk.W, "expandible": False}
        ]
        self.tabla_empresas.cabecera(columnas)
        self.tabla_empresas.tabla.bind("<Double-1>", self._on_seleccionar)
        
        # Botones
        self.frame_botones = ttk.Frame(self.frame_contenido)
        self.frame_botones.pack(fill="x")
        
        ttk.Button(self.frame_botones, text="Salir", command=self.app.quit).pack(side="right", padx=5)
        ttk.Button(self.frame_botones, text="Seleccionar", command=self._on_seleccionar).pack(side="right", padx=5)
    
    def inicializar(self):
        self._cargar_empresas()
    
    def _cargar_empresas(self):
        empresas = self.controlador.obtener_empresas()
        if not empresas:
            self.mostrar_mensaje("error", "No se pudieron cargar las empresas.")
            return
        
        # Preparación de datos optimizada (list comprehension / generator)
        datos_tabla = [
            (id_empresa, e.nif, e.nombre, e.tipo) 
            for id_empresa, e in sorted(empresas.items())
        ]
        self.tabla_empresas.insertar(datos_tabla)
    
    def _on_seleccionar(self, event=None):
        valores = self.tabla_empresas.seleccionar()
        if not valores:
            self.mostrar_mensaje("warning", "Debe seleccionar una empresa.")
            return
        
        if self.controlador.seleccionar_empresa(int(valores[0])):
            self.app.mostrar_frame("seleccion_archivo")
        else:
            self.mostrar_mensaje("error", "Error al seleccionar la empresa.")