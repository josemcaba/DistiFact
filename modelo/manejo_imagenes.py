# modelo/manejo_imagenes.py
# import os
import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import pytesseract
from typing import Tuple, Optional

class ManejadorImagenes:
    def __init__(self, mensaje_callback=None):
        self._mensaje_callback = mensaje_callback
    
    def _mensaje(self, tipo: str, mensaje: str):
        if self._mensaje_callback:
            self._mensaje_callback(tipo, mensaje)
        else:
            print(f"[{tipo}] {mensaje}")

    def detectar_orientacion(self, imagen: np.ndarray) -> int:
        """Detecta la orientación de la imagen usando Tesseract"""
        try:
            pil_image = Image.fromarray(imagen)
            osd = pytesseract.image_to_osd(pil_image)
            for line in osd.split("\n"):
                if "Rotate" in line:
                    return int(line.split(":")[-1].strip())
        except Exception as e:
            self._mensaje("error", f"Error detectando orientación: {str(e)}")
        return 0

    def rotar_imagen(self, imagen: np.ndarray, angulo: int) -> np.ndarray:
        """Rota la imagen según el ángulo especificado"""
        if angulo == 90:
            return cv2.rotate(imagen, cv2.ROTATE_90_CLOCKWISE)
        elif angulo == 180:
            return cv2.rotate(imagen, cv2.ROTATE_180)
        elif angulo == 270:
            return cv2.rotate(imagen, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return imagen

    def extraer_imagen_pdf(self, pdf_path: str) -> Tuple[Optional[np.ndarray], int]:
        """Extrae la primera imagen de un PDF"""
        try:
            with fitz.open(pdf_path) as pdf_doc:
                if pdf_doc.page_count == 0:
                    self._mensaje("error", "El PDF no tiene páginas")
                    return None, 0
                
                img_list = pdf_doc.get_page_images(0)
                if not img_list:
                    self._mensaje("error", "No se encontraron imágenes en la primera página")
                    return None, 0
                
                xref = img_list[0][0]
                base_imagen = pdf_doc.extract_image(xref)
                imagen_bytes = base_imagen["image"]
                imagen = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_COLOR)
                
                # Detectar y corregir orientación
                angulo = self.detectar_orientacion(imagen)
                return self.rotar_imagen(imagen, angulo), angulo
                
        except Exception as e:
            self._mensaje("error", f"Error extrayendo imagen: {str(e)}")
            return None, 0

    def set_mensaje_callback(self, callback):
        self._mensaje_callback = callback