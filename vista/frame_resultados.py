"""
Módulo que contiene la clase FrameResultados para mostrar los resultados del procesamiento.
"""
import tkinter as tk
from tkinter import ttk
import os
from typing import Dict, Any, Optional, List
import extractores.conceptos_factura as KEY
from vista.frame_base import FrameBase
from modelo.factura import Factura


class FrameResultados(FrameBase):
    """
    Frame para mostrar los resultados del procesamiento de facturas.
    """
    nombre = "resultados"
    
    def _obtener_titulo(self) -> str:
        """Retorna el título del frame."""
        return "Resultados del Procesamiento"
    
    def _inicializar_componentes(self):
        """Inicializa los componentes del frame."""
        super()._inicializar_componentes()
        
        # Contenedor principal
        self.frame_contenido = ttk.Frame(self)
        self.frame_contenido.pack(fill="both", expand=True)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.frame_contenido)
        self.notebook.pack(fill="both", expand=True, pady=10)
        
        # Pestaña de facturas correctas
        self.tab_correctas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_correctas, text="Facturas Correctas")
        
        # Pestaña de facturas con errores
        self.tab_errores = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_errores, text="Facturas con Errores")
        
        # Configurar tablas
        self._configurar_tabla_correctas()
        self._configurar_tabla_errores()
        
        # Frame para botones
        self.frame_botones = ttk.Frame(self.frame_contenido)
        self.frame_botones.pack(fill="x", pady=10)
        
        # Botón de exportar
        self.btn_exportar = ttk.Button(
            self.frame_botones,
            text="Exportar a Excel",
            command=self._on_exportar
        )
        self.btn_exportar.pack(side="right", padx=5)
        
        # Botón de nueva consulta
        self.btn_nueva = ttk.Button(
            self.frame_botones,
            text="Nueva Consulta",
            command=lambda: self.app.mostrar_frame("seleccion_empresa")
        )
        self.btn_nueva.pack(side="right", padx=5)
    
    def _configurar_tabla_correctas(self):
        """Configura la tabla de facturas correctas."""
        # Frame para la tabla
        frame_tabla = ttk.Frame(self.tab_correctas)
        frame_tabla.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(frame_tabla)
        scrollbar_y.pack(side="right", fill="y")
        
        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(frame_tabla, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")
        
        # Columnas de la tabla
        columnas = [
            "Núm. Factura", "Fecha", "NIF", "Empresa", 
            "Base IVA", "Tipo IVA", "Cuota IVA", 
            "Total", "Observaciones"
        ]
        
        # Crear Treeview
        self.tabla_correctas = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # Configurar scrollbars
        scrollbar_y.config(command=self.tabla_correctas.yview)
        scrollbar_x.config(command=self.tabla_correctas.xview)
        
        # Configurar encabezados
        for col in columnas:
            self.tabla_correctas.heading(col, text=col)
            self.tabla_correctas.column(col, width=50, anchor="center")
        
        # Ajustar columnas específicas
        self.tabla_correctas.column("Observaciones", width=100, anchor="w")
        
        # Empaquetar tabla
        self.tabla_correctas.pack(side="left", fill="both", expand=True)
    
    def _configurar_tabla_errores(self):
        """Configura la tabla de facturas con errores."""
        # Frame para la tabla
        frame_tabla = ttk.Frame(self.tab_errores)
        frame_tabla.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(frame_tabla)
        scrollbar_y.pack(side="right", fill="y")
        
        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(frame_tabla, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")
        
        # Columnas de la tabla
        columnas = [
            "Núm. Factura", "Fecha", "NIF", "Empresa", 
            "Base IVA", "Tipo IVA", "Cuota IVA", 
            "Total", "Errores"
        ]
        
        # Crear Treeview
        self.tabla_errores = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # Configurar scrollbars
        scrollbar_y.config(command=self.tabla_errores.yview)
        scrollbar_x.config(command=self.tabla_errores.xview)
        
        # Configurar encabezados
        for col in columnas:
            self.tabla_errores.heading(col, text=col)
            self.tabla_errores.column(col, width=100, anchor="center")
        
        # Ajustar columnas específicas
        self.tabla_errores.column("Errores", width=200, anchor="w")
        
        # Empaquetar tabla
        self.tabla_errores.pack(side="left", fill="both", expand=True)
    
    def inicializar(self):
        """Inicializa el frame cuando se muestra."""
        # Obtener resultados del procesamiento
        facturas_correctas, facturas_con_errores = self.controlador.obtener_resultados()
        
        # Limpiar tablas
        self._limpiar_tablas()
        
        # Cargar datos en las tablas
        self._cargar_facturas_correctas(facturas_correctas)
        self._cargar_facturas_con_errores(facturas_con_errores)
        
        # Actualizar pestañas con conteo
        self.notebook.tab(0, text=f"Facturas Correctas ({len(facturas_correctas)})")
        self.notebook.tab(1, text=f"Facturas con Errores ({len(facturas_con_errores)})")
    
    def _limpiar_tablas(self):
        """Limpia las tablas de resultados."""
        # Limpiar tabla de facturas correctas
        for item in self.tabla_correctas.get_children():
            self.tabla_correctas.delete(item)
        
        # Limpiar tabla de facturas con errores
        for item in self.tabla_errores.get_children():
            self.tabla_errores.delete(item)
    
    def _cargar_facturas_correctas(self, facturas: List[Factura]):
        """
        Carga las facturas correctas en la tabla.
        
        Args:
            facturas: Lista de facturas correctas
        """
        for factura in facturas:
            datos = factura.datos
            
            # Preparar valores para la tabla
            valores = [
                datos.get(KEY.NUM_FACT, ""),
                datos.get(KEY.FECHA_FACT, ""),
                datos.get(KEY.NIF, ""),
                datos.get(KEY.EMPRESA, ""),
                datos.get(KEY.BASE_IVA, ""),
                datos.get(KEY.TIPO_IVA, ""),
                datos.get(KEY.CUOTA_IVA, ""),
                datos.get(KEY.TOTAL_FACT, ""),
                ", ".join(factura.observaciones) if factura.observaciones else ""
            ]
            
            # Insertar en la tabla
            self.tabla_correctas.insert("", "end", values=valores)
    
    def _cargar_facturas_con_errores(self, facturas: List[Factura]):
        """
        Carga las facturas con errores en la tabla.
        
        Args:
            facturas: Lista de facturas con errores
        """
        for factura in facturas:
            datos = factura.datos
            
            # Preparar valores para la tabla
            valores = [
                datos.get(KEY.NUM_FACT, ""),
                datos.get(KEY.FECHA_FACT, ""),
                datos.get(KEY.NIF, ""),
                datos.get(KEY.EMPRESA, ""),
                datos.get(KEY.BASE_IVA, ""),
                datos.get(KEY.TIPO_IVA, ""),
                datos.get(KEY.CUOTA_IVA, ""),
                datos.get(KEY.TOTAL_FACT, ""),
                ", ".join(factura.errores) if factura.errores else ""
            ]
            
            # Insertar en la tabla
            self.tabla_errores.insert("", "end", values=valores)
    
    def _on_exportar(self):
        """Maneja el evento de exportar a Excel."""
        # Obtener ruta del archivo original
        ruta_original = self.controlador.obtener_ruta_archivo()
        
        if not ruta_original:
            self.mostrar_mensaje("error", "No hay archivo procesado.")
            return
        
        # Generar rutas para los archivos Excel automáticamente
        if ruta_original.lower().endswith(".pdf"):
            ruta_base = ruta_original.replace(".pdf", "")
        elif ruta_original.lower().endswith(".xlsx"):
            ruta_base = ruta_original.replace(".xlsx", "")
        elif ruta_original.lower().endswith(".xls"):
            ruta_base = ruta_original.replace(".xls", "")
        else:
            ruta_base = ruta_original
        
        # Exportar a Excel usando la ruta base generada automáticamente
        try:
            resultado = self.controlador.exportar_resultados(ruta_base)
        except Exception as e:
            self.mostrar_mensaje("error", f"Error en exportación: {str(e)}")
            resultado = {}
        
        if resultado:
            mensaje = f"Resultados exportados correctamente a:\n"
            if "correctas" in resultado:
                mensaje += f"- {resultado['correctas']}\n"
            if "errores" in resultado:
                mensaje += f"- {resultado['errores']}"
                
            self.mostrar_mensaje(
                "info", 
                mensaje,
                "Exportación Exitosa"
            )
        else:
            self.mostrar_mensaje(
                "error", 
                "Error al exportar los resultados.",
                "Error de Exportación"
            )
