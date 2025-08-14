"""
Módulo que contiene la clase ExportadorExcel para exportar facturas a Excel.
"""
import pandas as pd
from typing import List, Dict, Any
import extractores.conceptos_factura as KEY
from modelo.factura import Factura


class ExportadorExcel:
    """
    Clase que exporta facturas a archivos Excel.
    """
    def __init__(self):
        """Inicializa el exportador de Excel."""
        self._mensaje_callback = None
    
    def set_mensaje_callback(self, callback):
        """
        Establece la función de callback para mostrar mensajes.
        
        Args:
            callback: Función para mostrar mensajes (tipo, mensaje)
        """
        self._mensaje_callback = callback
    
    def _mostrar_mensaje(self, tipo: str, mensaje: str) -> None:
        """
        Muestra un mensaje usando el callback si está disponible.
        
        Args:
            tipo: Tipo de mensaje ('info', 'error')
            mensaje: Contenido del mensaje
        """
        if self._mensaje_callback:
            self._mensaje_callback(tipo, mensaje)
        else:
            print(f"{tipo.upper()}: {mensaje}")
    
    def exportar(self, facturas_correctas: List[Factura], 
                facturas_con_errores: List[Factura], 
                ruta_base: str) -> Dict[str, str]:
        """
        Exporta las facturas a archivos Excel.
        
        Args:
            facturas_correctas: Lista de facturas correctas
            facturas_con_errores: Lista de facturas con errores
            ruta_base: Ruta base para los archivos Excel
            
        Returns:
            Diccionario con las rutas de los archivos generados
        """
        rutas = {}
        
        # Definir las columnas para el DataFrame
        columnas = [
            KEY.NUM_FACT, KEY.FECHA_FACT, KEY.FECHA_OPER, KEY.CONCEPTO,
            KEY.BASE_IVA, KEY.TIPO_IVA, KEY.CUOTA_IVA, 
            KEY.BASE_IRPF, KEY.TIPO_IRPF, KEY.CUOTA_IRPF,
            KEY.BASE_RE, KEY.TIPO_RE, KEY.CUOTA_RE,
            KEY.NIF, KEY.EMPRESA
        ]
        
        # Exportar facturas correctas
        if facturas_correctas:
            # Convertir las facturas a diccionarios
            datos_correctas = [factura.to_dict() for factura in facturas_correctas]
            
            # Crear DataFrame y ordenar por número de factura
            df_correctas = pd.DataFrame(datos_correctas, columns=columnas + ["Observaciones"])
            df_correctas = df_correctas.sort_values(by=columnas[0])
            
            # Generar ruta para el archivo
            ruta_correctas = f"{ruta_base}_correctas.xlsx"
            
            # Exportar a Excel
            df_correctas.to_excel(ruta_correctas, index=False)
            
            # Guardar ruta en el diccionario de resultados
            rutas["correctas"] = ruta_correctas
            
            # Mostrar mensaje de éxito
            self._mostrar_mensaje('info', f"Se han exportado {len(facturas_correctas)} facturas correctas.")
        else:
            self._mostrar_mensaje('info', "No hay facturas correctas para exportar.")
        
        # Exportar facturas con errores
        if facturas_con_errores:
            # Convertir las facturas a diccionarios
            datos_errores = [factura.to_dict() for factura in facturas_con_errores]
            
            # Crear DataFrame y ordenar por número de factura
            df_errores = pd.DataFrame(datos_errores, columns=columnas + ["Errores"])
            df_errores = df_errores.sort_values(by=columnas[0])
            
            # Generar ruta para el archivo
            ruta_errores = f"{ruta_base}_errores.xlsx"
            
            # Exportar a Excel
            df_errores.to_excel(ruta_errores, index=False)
            
            # Guardar ruta en el diccionario de resultados
            rutas["errores"] = ruta_errores
            
            # Mostrar mensaje de éxito
            self._mostrar_mensaje('info', f"Se han exportado {len(facturas_con_errores)} facturas con errores.")
        else:
            self._mostrar_mensaje('info', "No hay facturas con errores para exportar.")
        
        return rutas
