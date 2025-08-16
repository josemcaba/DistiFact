"""
Módulo para visualizar los rectángulos definidos en las imágenes de un PDF.
Adaptado para la estructura orientada a objetos de la aplicación.
"""
import fitz  # PyMuPDF
from .extractor_imagenes import ExtractorImagenes
from .extractor_texto import ExtractorTexto
from .exhibidor_imagenes import ExhibidorImagenes

# import ft_imagenes as fti

class VisualizadorRectangulos:
    """
    Clase para visualizar los rectángulos definidos en las imágenes de un PDF.
    """
    def __init__(self, controlador):
        """
        Inicializa el visualizador de rectángulos.
        
        Args:
            controlador: Instancia del controlador de la aplicación
        """
        self.controlador = controlador
        self.extractor = ExtractorImagenes()
        self.ocr = ExtractorTexto()
        self.exhibidor = ExhibidorImagenes()

    def _mensaje(self, tipo: str, mensaje: str):
        if self.controlador and hasattr(self.controlador, '_mensaje_callback'):
            self.controlador._mensaje_callback(tipo, mensaje)
        else:
            print(f"[{tipo}] {mensaje}")

    def visualizar_rectangulos(self, ruta_pdf, empresa):
        """
        Visualiza los rectángulos definidos en las imágenes de un PDF.
        
        Args:
            ruta_pdf: Ruta al archivo PDF
            empresa: Diccionario con información de la empresa
        
        Returns:
            True si se completó correctamente, False en caso contrario
        """
        if not empresa:
            self._mensaje("error", "Datos de empresa inválidos")
            return False
        
        # Cargar rectángulos
        rectangulos = self.extractor.cargar_rectangulos_json(empresa["nif"])
        if not rectangulos:
            self._mensaje("error", f"No se encontraron rectángulos para la empresa {empresa['nombre']}.")
            return False
        
        angulo = rectangulos["angulo"]
        
        try:
            with fitz.open(ruta_pdf) as pdf_doc:
                total_paginas = pdf_doc.page_count
                for n_pag in range(total_paginas):
                    imagen_pag, angulo = self.extractor.extraer_imagen_de_pdf(pdf_doc, n_pag, angulo)
                    imagenes = self.extractor.extraer_imagenes_de_rectangulos(imagen_pag, rectangulos)
                    self._mensaje("", f"\n>>>>> Página {n_pag+1}")
                    for imagen in imagenes:
                        _ = self.ocr.extraer_texto_de_imagen(imagen[0], imagen[1], printTexto=True)
                        self.exhibidor.mostrar_imagen(imagen[0], window_name=f">>>>> Pagina {n_pag+1}")
            return True
        except Exception as e:
            self._mensaje("error", f"Error al visualizar rectángulos: {str(e)}")
            return False
