"""
Módulo que contiene la clase Controlador, que coordina el modelo y la vista.
"""
from typing import Dict, Any, Optional, List, Tuple, Callable

# Importamos clases del modelo
from modelo.cargar_empresas import EmpresasManager
from modelo.empresa import Empresa, EmpresaManager
from modelo.factura import Factura
from modelo.procesador import ProcesadorFacturas
from modelo.clasificador import ClasificadorFacturas
from modelo.exportador import ExportadorExcel
from modelo.vizualizador_rectangulos import VisualizadorRectangulos
from modelo.creador_rectangulos import CreadorRectangulos

class Controlador:
    """
    Clase que coordina la interacción entre el modelo y la vista.
    """
    def __init__(self):
        """Inicializa el controlador."""
        # Instancias del modelo
        self._empresas_manager = EmpresasManager()
        self._empresa_manager = EmpresaManager()
        self._procesador = ProcesadorFacturas()
        self._clasificador = ClasificadorFacturas()
        self._exportador = ExportadorExcel()
        self._visualizador = VisualizadorRectangulos(self)
        self._creador = CreadorRectangulos(self)
        
        # Estado actual
        self._empresa_actual = None
        self._ruta_archivo = None
        self._facturas = []
        self._facturas_correctas = []
        self._facturas_con_errores = []
    
    def cargar_empresas(self, archivo_json):
        datos = (
			(575, '23645938F', 'ACIEGO ESCOBAR, MARIA JOSE', 'PDF Imagenes'), 
			(229, '36532215A', "ALAMINOS PEREZ, FRANCISCO JAVIER", 'Excel'),
			(123, '12345678A', "GARCÍA LÓPEZ, JUAN", 'Word'),
			(456, '87654321B', "MARTÍNEZ SÁNCHEZ, ANA", 'PDF'),
			(789, '11223344C', "RODRÍGUEZ FERNÁNDEZ, CARLOS", 'Excel')
		)
        datos = datos * 3  # Multiplicar para tener más datos
        print(type(datos[0][0]))
        return datos    

    def iniciar(self, ruta_json: str = "empresas.json") -> bool:
        """
        Inicia la aplicación cargando las empresas.
        
        Args:
            ruta_json: Ruta al archivo JSON con los datos de empresas
            
        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        return self._empresa_manager.cargar_empresas(ruta_json)
    
    def obtener_empresas(self) -> Dict[int, Empresa]:
        """
        Obtiene el diccionario de empresas.
        
        Returns:
            Diccionario con las empresas cargadas
        """
        return self._empresa_manager.listar_empresas()
    
    def seleccionar_empresa(self, id_empresa: int) -> bool:
        """
        Selecciona una empresa por su ID.
        
        Args:
            id_empresa: ID de la empresa a seleccionar
            
        Returns:
            True si la selección fue exitosa, False en caso contrario
        """
        empresa = self._empresa_manager.obtener_empresa(id_empresa)
        if empresa:
            self._empresa_actual = empresa
            return True
        return False
    
    def obtener_empresa_actual(self) -> Optional[Empresa]:
        """
        Obtiene la empresa actualmente seleccionada.
        
        Returns:
            Instancia de Empresa o None si no hay empresa seleccionada
        """
        return self._empresa_actual
    
    def establecer_ruta_archivo(self, ruta: str) -> None:
        """
        Establece la ruta del archivo a procesar.
        
        Args:
            ruta: Ruta al archivo
        """
        self._ruta_archivo = ruta
    
    def obtener_ruta_archivo(self) -> Optional[str]:
        """
        Obtiene la ruta del archivo actual.
        
        Returns:
            Ruta del archivo o None si no hay archivo
        """
        return self._ruta_archivo
    
    def configurar_callbacks(self, progreso_callback: Callable[[int, int], None], 
                           mensaje_callback: Callable[[str, str], None]) -> None:
        """
        Configura las funciones de callback para reportar progreso y mensajes.
        
        Args:
            progreso_callback: Función para reportar progreso (página actual, total)
            mensaje_callback: Función para mostrar mensajes (tipo, mensaje)
        """
        self._procesador.set_callbacks(progreso_callback, mensaje_callback)
        self._exportador.set_mensaje_callback(mensaje_callback)
        self._creador.set_mensaje_callback(mensaje_callback)
    
    def procesar_archivo(self) -> List[Factura]:
        """
        Procesa el archivo actual.
        
        Returns:
            Lista de facturas procesadas o None si hubo error
        """
        if not self._empresa_actual or not self._ruta_archivo:
            return None
        
        # Procesar archivo
        self._facturas = self._procesador.procesar_archivo(self._ruta_archivo, self._empresa_actual)
        
        if not self._facturas:
            return None
        
        # Clasificar facturas
        self._facturas_correctas, self._facturas_con_errores = self._clasificador.clasificar(self._facturas)
        
        return self._facturas
    
    def obtener_resultados(self) -> Tuple[List[Factura], List[Factura]]:
        """
        Obtiene los resultados del procesamiento.
        
        Returns:
            Tupla con dos listas: (facturas_correctas, facturas_con_errores)
        """
        return self._facturas_correctas, self._facturas_con_errores
    
    def exportar_resultados(self, ruta_excel: str) -> Dict[str, str]:
        """
        Exporta los resultados a Excel.
        
        Args:
            ruta_excel: Ruta base para los archivos Excel
            
        Returns:
            Diccionario con las rutas de los archivos generados o vacío si hubo error
        """
        if not self._facturas_correctas and not self._facturas_con_errores:
            return {}
        
        try:
            # Exportar a Excel
            rutas = self._exportador.exportar(
                self._facturas_correctas,
                self._facturas_con_errores,
                ruta_excel
            )
            
            return rutas
        except Exception:
            return {}
    
    def visualizar_rectangulos(self, ruta_pdf: str, empresa_dict: Dict[str, Any]) -> bool:
        """
        Visualiza los rectángulos definidos en las imágenes de un PDF.
        
        Args:
            ruta_pdf: Ruta al archivo PDF
            empresa_dict: Diccionario con información de la empresa
            
        Returns:
            True si se completó correctamente, False en caso contrario
        """
        return self._visualizador.visualizar_rectangulos(ruta_pdf, empresa_dict)
    
    def crear_rectangulos(self, ruta_pdf: str, empresa_dict: Dict[str, Any]) -> bool:
        """
        Crea los rectángulos en las imágenes de un PDF.
        
        Args:
            ruta_pdf: Ruta al archivo PDF
            empresa_dict: Diccionario con información de la empresa
            
        Returns:
            True si se completó correctamente, False en caso contrario
        """
        return self._creador.crear(ruta_pdf, empresa_dict)
