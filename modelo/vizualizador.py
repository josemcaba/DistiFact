"""
Módulo para visualizar los rectángulos definidos en las imágenes de un PDF.
Adaptado para la estructura orientada a objetos de la aplicación.
"""
import fitz  # PyMuPDF
import ft_imagenes as fti
from ft_mensajes_POO import msg

class VisualizadorRectangulos:
    """
    Clase para visualizar los rectángulos definidos en las imágenes de un PDF.
    """
    def __init__(self, controlador=None):
        """
        Inicializa el visualizador de rectángulos.
        
        Args:
            controlador: Instancia del controlador de la aplicación
        """
        self.controlador = controlador
    
    def visualizar(self, ruta_pdf, empresa):
        """
        Visualiza los rectángulos definidos en las imágenes de un PDF.
        
        Args:
            ruta_pdf: Ruta al archivo PDF
            empresa: Diccionario con información de la empresa
        
        Returns:
            True si se completó correctamente, False en caso contrario
        """
        if not ruta_pdf or not empresa:
            msg.error("No se ha seleccionado un archivo o empresa válida.")
            return False
        
        # Cargar rectángulos
        rectangulos = fti.cargar_rectangulos_json(empresa["nif"])
        if not rectangulos:
            msg.error(f"No se encontraron rectángulos para la empresa {empresa['nombre']}.")
            return False
        
        angulo = rectangulos["angulo"]
        
        try:
            with fitz.open(ruta_pdf) as pdf_doc:
                total_paginas = len(pdf_doc)
                for n_pag in range(total_paginas):
                    imagen_pag = fti.extraer_imagen_de_la_pagina(pdf_doc, n_pag, angulo)
                    imagenes = fti.extraer_imagenes_de_los_rectangulos(imagen_pag, rectangulos)
                    msg.info(f"\n>>>>> Página {n_pag+1}")
                    for imagen in imagenes:
                        texto = fti.extraer_texto_de_imagen(imagen[0], imagen[1], verRectangulos=True)
            
            return True
        except Exception as e:
            msg.error(f"Error al visualizar rectángulos: {str(e)}")
            return False
