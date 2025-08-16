# modelo/manejo_imagenes.py

import json
import cv2
import numpy as np
from PIL import Image
import pytesseract
from typing import Tuple, Optional

class ExtractorImagenes:
    def __init__(self, mensaje_callback=None):
        self._mensaje_callback = mensaje_callback
    
    def _mensaje(self, tipo: str, mensaje: str):
        if self._mensaje_callback:
            self._mensaje_callback(tipo, mensaje)
        else:
            print(f"[{tipo}] {mensaje}")

    def cargar_rectangulos_json(self, nif, ruta_json="rectangulos.json"):
        try:
            with open(ruta_json, "r", encoding='utf-8') as archivo:
                coords = json.load(archivo)
            rectangles = coords[nif]
            return rectangles
        except FileNotFoundError:
            self._mensaje("error", f'Archivo "{ruta_json}" no encontrado.')
        except (json.JSONDecodeError):
            self._mensaje("error", f'El archivo "{ruta_json}" tiene un formato inválido.')
        except (KeyError):
            self._mensaje("error", f'El archivo "{ruta_json}" no contiene la empresa "{nif}"')
        return

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

    def extraer_imagen_de_pdf(self, pdf_doc, n_pag=0, angulo=None) -> Tuple[Optional[np.ndarray], int]:
        """Extrae la primera imagen de una página de un PDF"""
        try:
            if pdf_doc.page_count == 0:
                self._mensaje("error", "El PDF no tiene páginas")
                return None, None
            
            img_list = pdf_doc.get_page_images(n_pag)
            if not img_list:
                self._mensaje("error", "No se encontraron imágenes en la primera página")
                return None, None
            
            xref = img_list[0][0]
            base_imagen = pdf_doc.extract_image(xref)
            imagen_bytes = base_imagen["image"]
            imagen = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_COLOR)
            
            # Detectar y corregir orientación
            if angulo is None:
                angulo = self.detectar_orientacion(imagen)
            return self.rotar_imagen(imagen, angulo), angulo
        except Exception as e:
            self._mensaje("error", f"Error extrayendo imagen: {str(e)}")
            return None, None

    def extraer_imagenes_de_rectangulos(self, imagen, rectangulos):
        imagenes = []
        height, width = imagen.shape[:2]

        # Recortar y mostrar cada trozo de imagen según las coordenadas del JSON
        for key, coords in rectangulos.items():
            if not key.startswith("rectangulo"):
                continue
            x1, y1 = coords["x1"], coords["y1"]
            x2, y2 = coords["x2"], coords["y2"]

            # Verificar que las coordenadas estén dentro de los límites de la imagen
            if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
                self._mensaje("error", f"Coordenadas {key} fuera de los límites de la imagen.")
                continue
            
            cropped_image = imagen[y1:y2, x1:x2]  # Recortar la región de la imagen
            tesseract_config = coords["tesseract"]
            imagenes.append([cropped_image, tesseract_config])
        return (imagenes)

    def set_mensaje_callback(self, callback):
        self._mensaje_callback = callback