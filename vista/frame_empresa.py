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
         
        # Frame para la tabla
        self.frame_tabla = ttk.Frame(self.frame_contenido)
        self.frame_tabla.pack(fill="both", expand=True, pady=10, padx=10)
        
        # Crear tabla utilizando la clase Tabla
        from vista.Tabla import Tabla  # Importar aquí para evitar problemas de importación circular
        
        self.tabla_empresas = Tabla(self.frame_tabla)
        self.tabla_empresas.pack(fill="both", expand=True)
        
        # Configurar columnas de la tabla
        columnas = [
            {"nombre": "ID", "ancho": 50, "alineacion": tk.CENTER, "expandible": False},
            {"nombre": "Nombre", "ancho": 175, "alineacion": tk.W, "expandible": True},
            {"nombre": "NIF", "ancho": 100, "alineacion": tk.CENTER, "expandible": False},
            {"nombre": "Tipo", "ancho": 100, "alineacion": tk.W, "expandible": False}
        ]
        self.tabla_empresas.cabecera(columnas)
        
        # Vincular doble clic a selección
        self.tabla_empresas.tabla.bind("<Double-1>", self._on_seleccionar)
        
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
        # Cargar empresas en la tabla
        self._cargar_empresas()
    
    def _cargar_empresas(self):
        """Carga las empresas en la tabla."""
        # Limpiar tabla (eliminar todas las filas)
        for item in self.tabla_empresas.tabla.get_children():
            self.tabla_empresas.tabla.delete(item)
        
        # Obtener empresas del controlador
        empresas = self.controlador.obtener_empresas()
        
        if not empresas:
            self.mostrar_mensaje("error", "No se pudieron cargar las empresas.")
            return
        
        # Agregar empresas a la tabla
        datos_tabla = []
        for id_empresa, empresa in sorted(empresas.items()):
            datos_tabla.append((
                id_empresa,
                empresa.nombre,
                empresa.nif,
                empresa.tipo
            ))
        
        self.tabla_empresas.insertar(datos_tabla)
    
    def _on_seleccionar(self, event=None):
        """
        Maneja el evento de selección de empresa.
        
        Args:
            event: Evento que desencadenó la acción (opcional)
        """
        # Obtener fila seleccionada de la tabla
        valores = self.tabla_empresas.seleccionar()
        
        if not valores:
            self.mostrar_mensaje("warning", "Debe seleccionar una empresa.")
            return
        
        # Los valores vienen en el orden: ID, Nombre, NIF, Tipo
        id_empresa = int(valores[0])
        
        # Seleccionar empresa en el controlador
        if self.controlador.seleccionar_empresa(id_empresa):
            # Avanzar al siguiente frame
            self.app.mostrar_frame("seleccion_archivo")
        else:
            self.mostrar_mensaje("error", "Error al seleccionar la empresa.")