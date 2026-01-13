"""
Módulo que contiene la clase FrameResultados para mostrar los resultados del procesamiento.
"""
from tkinter import ttk
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
        
        # Configurar tablas usando método común
        columnas_base = self._obtener_columnas_base()
        columnas_correctas = columnas_base + [
            {"nombre": "Observaciones", "ancho": 150, "alineacion": "w", "expandible": True}
        ]
        columnas_errores = columnas_base + [
            {"nombre": "Errores", "ancho": 150, "alineacion": "w", "expandible": True}
        ]
        
        self.tabla_correctas = self._crear_tabla_en_frame(self.tab_correctas, columnas_correctas)
        self.tabla_errores = self._crear_tabla_en_frame(self.tab_errores, columnas_errores)
        
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
    
    def _obtener_columnas_base(self):
        """Devuelve las columnas comunes para ambas tablas."""
        return [
            {"nombre": "Núm. Factura", "ancho": 100, "alineacion": "w", "expandible": False},
            {"nombre": "Fecha", "ancho": 100, "alineacion": "center", "expandible": False},
            {"nombre": "NIF", "ancho": 100, "alineacion": "center", "expandible": False},
            {"nombre": "Empresa", "ancho": 300, "alineacion": "w", "expandible": False},
            {"nombre": "Base IVA", "ancho": 75, "alineacion": "e", "expandible": False},
            {"nombre": "Tipo IVA", "ancho": 75, "alineacion": "e", "expandible": False},
            {"nombre": "Cuota IVA", "ancho": 75, "alineacion": "e", "expandible": False},
            {"nombre": "Total", "ancho": 75, "alineacion": "e", "expandible": False}
        ]
    
    def _crear_tabla_en_frame(self, frame_padre, columnas):
        """
        Crea y configura una tabla en el frame proporcionado.
        
        Args:
            frame_padre: Frame donde se colocará la tabla
            columnas: Lista de diccionarios con configuración de columnas
            
        Returns:
            Instancia de Tabla configurada
        """
        # Frame para la tabla
        frame_tabla = ttk.Frame(frame_padre)
        frame_tabla.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Importar la clase Tabla
        from vista.Tabla import Tabla
        
        # Crear tabla utilizando la clase Tabla
        tabla = Tabla(frame_tabla)
        tabla.pack(fill="both", expand=True)
        
        # Configurar columnas de la tabla
        tabla.cabecera(columnas)
        
        return tabla
    
    def inicializar(self):
        """Inicializa el frame cuando se muestra."""
        # Obtener resultados del procesamiento
        facturas_correctas, facturas_con_errores = self.controlador.obtener_resultados()
        
        # Limpiar tablas
        self._limpiar_tabla(self.tabla_correctas)
        self._limpiar_tabla(self.tabla_errores)
        
        # Cargar datos en las tablas
        self._cargar_facturas_en_tabla(self.tabla_correctas, facturas_correctas, es_errores=False)
        self._cargar_facturas_en_tabla(self.tabla_errores, facturas_con_errores, es_errores=True)
        
        # Actualizar pestañas con conteo
        self.notebook.tab(0, text=f"Facturas Correctas ({len(facturas_correctas)})")
        self.notebook.tab(1, text=f"Facturas con Errores ({len(facturas_con_errores)})")
    
    def _limpiar_tabla(self, tabla):
        """Limpia una tabla específica."""
        for item in tabla.tabla.get_children():
            tabla.tabla.delete(item)
    
    def _cargar_facturas_en_tabla(self, tabla, facturas, es_errores=False):
        """
        Carga las facturas en la tabla especificada.
        
        Args:
            tabla: Instancia de Tabla donde cargar los datos
            facturas: Lista de facturas a cargar
            es_errores: Indica si son facturas con errores (para determinar la columna final)
        """
        datos_tabla = []
        
        for factura in facturas:
            datos = factura.datos
            
            # Preparar valores base (comunes a ambas tablas)
            valores = [
                datos.get(KEY.NUM_FACT, ""),
                datos.get(KEY.FECHA_FACT, ""),
                datos.get(KEY.NIF, ""),
                datos.get(KEY.EMPRESA, ""),
                datos.get(KEY.BASE_IVA, ""),
                datos.get(KEY.TIPO_IVA, ""),
                datos.get(KEY.CUOTA_IVA, ""),
                datos.get(KEY.TOTAL_FACT, ""),
            ]
            
            # Añadir columna específica según el tipo de tabla
            if es_errores:
                valores.append(", ".join(factura.errores) if factura.errores else "")
            else:
                valores.append(", ".join(factura.observaciones) if factura.observaciones else "")
            
            datos_tabla.append(valores)
        
        # Insertar todos los datos en la tabla
        tabla.insertar(datos_tabla)
    
    def _on_exportar(self):
        """Maneja el evento de exportar a Excel."""
        # Obtener ruta del archivo original
        ruta_original = self.controlador.obtener_ruta_archivo()
        
        if not ruta_original:
            self.mostrar_mensaje("error", "No hay archivo procesado.")
            return
        
        # Generar rutas para los archivos Excel automáticamente
        ruta_base = self._obtener_ruta_base_exportacion(ruta_original)
        
        # Exportar a Excel usando la ruta base generada automáticamente
        try:
            resultado = self.controlador.exportar_resultados(ruta_base)
        except Exception as e:
            self.mostrar_mensaje("error", f"Error en exportación: {str(e)}")
            resultado = {}
        
        # Mostrar resultado de la exportación
        self._mostrar_resultado_exportacion(resultado)
    
    def _obtener_ruta_base_exportacion(self, ruta_original):
        """
        Obtiene la ruta base para exportación eliminando la extensión del archivo.
        
        Args:
            ruta_original: Ruta completa del archivo original
            
        Returns:
            str: Ruta base sin extensión
        """
        if ruta_original.lower().endswith(".pdf"):
            return ruta_original.replace(".pdf", "")
        elif ruta_original.lower().endswith(".xlsx"):
            return ruta_original.replace(".xlsx", "")
        elif ruta_original.lower().endswith(".xls"):
            return ruta_original.replace(".xls", "")
        else:
            return ruta_original
    
    def _mostrar_resultado_exportacion(self, resultado):
        """
        Muestra el resultado de la operación de exportación.
        
        Args:
            resultado: Diccionario con los resultados de la exportación
        """
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