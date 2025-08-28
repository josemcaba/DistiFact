"""
Módulo que contiene la clase FrameSeleccionEmpresa para seleccionar una empresa.
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional

from vista.frame_base import FrameBase


class FrameSeleccionEmpresa(FrameBase):
    """
    Frame para seleccionar una empresa.
    """
    nombre = "seleccion_empresa"
    
    def _obtener_titulo(self) -> str:
        """Retorna el título del frame."""
        return "Selección de Empresa"
    
    def _inicializar_componentes(self):
        """Inicializa los componentes del frame."""
        super()._inicializar_componentes()
        
        # Contenedor principal
        self.frame_contenido = ttk.Frame(self)
        self.frame_contenido.pack(fill="both", expand=True)
         
        # Frame para la lista y scrollbar
        self.frame_lista = ttk.Frame(self.frame_contenido)
        self.frame_lista.pack(fill="both", expand=True, pady=10)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_lista)
        self.scrollbar.pack(side="right", fill="y")
        
        # Lista de empresas
        self.lista_empresas = tk.Listbox(
            self.frame_lista,
            height=10,
            width=50,
            yscrollcommand=self.scrollbar.set,
            font=("Arial", 10),
            selectmode=tk.SINGLE
        )
        self.lista_empresas.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.lista_empresas.yview)
        
        # Vincular doble clic a selección
        self.lista_empresas.bind("<Double-1>", self._on_seleccionar)
        
        # Frame para botones
        self.frame_botones = ttk.Frame(self.frame_contenido)
        self.frame_botones.pack(fill="x", pady=10)
        
        # Botón de seleccionar
        self.btn_seleccionar = ttk.Button(
            self.frame_botones,
            text="Seleccionar",
            command=self._on_seleccionar
        )
        self.btn_seleccionar.pack(side="right", padx=5)
        
        # Botón de salir
        self.btn_salir = ttk.Button(
            self.frame_botones,
            text="Salir",
            command=self.app.quit
        )
        self.btn_salir.pack(side="right", padx=5)
    
    def inicializar(self):
        """Inicializa el frame cuando se muestra."""
        # Cargar empresas
        self._cargar_empresas()
    
    def _cargar_empresas(self):
        """Carga las empresas en la lista."""
        # Limpiar lista
        self.lista_empresas.delete(0, tk.END)
        
        # Obtener empresas del controlador
        empresas = self.controlador.obtener_empresas()
        
        if not empresas:
            self.mostrar_mensaje("error", "No se pudieron cargar las empresas.")
            return
        
        # Agregar empresas a la lista
        for id_empresa, empresa in sorted(empresas.items()):
            self.lista_empresas.insert(tk.END, f"{id_empresa}: {empresa.nombre} ({empresa.nif})")
    
    def _on_seleccionar(self, event=None):
        """
        Maneja el evento de selección de empresa.
        
        Args:
            event: Evento que desencadenó la acción (opcional)
        """
        # Obtener índice seleccionado
        seleccion = self.lista_empresas.curselection()
        
        if not seleccion:
            self.mostrar_mensaje("warning", "Debe seleccionar una empresa.")
            return
        
        # Obtener texto seleccionado
        texto = self.lista_empresas.get(seleccion[0])
        
        # Extraer ID de empresa
        id_empresa = int(texto.split(":")[0])
        
        # Seleccionar empresa en el controlador
        if self.controlador.seleccionar_empresa(id_empresa):
            # Avanzar al siguiente frame
            self.app.mostrar_frame("seleccion_archivo")
        else:
            self.mostrar_mensaje("error", "Error al seleccionar la empresa.")
