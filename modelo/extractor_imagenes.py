# modelo/manejo_imagenes.py

import os
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
    
    def cargar_rectangulos_json(self, nif, ruta_json=None):
        """
        Carga los rectángulos del archivo JSON para un NIF específico.
        
        Args:
            nif: NIF de la empresa
            ruta_json: Ruta personalizada al archivo JSON (opcional)
                     Si no se proporciona, busca en datos/rectangulos.json
                     
        Returns:
            dict: Rectángulos para la empresa especificada o None en caso de error
        """
        try:
            # Si no se proporciona ruta, usar la ruta por defecto en el directorio datos
            if ruta_json is None:
                # Obtener el directorio del archivo actual (modelo/)
                current_dir = os.path.dirname(os.path.abspath(__file__))
                # Subir un nivel al directorio del proyecto (raíz)
                project_dir = os.path.dirname(current_dir)
                # Construir la ruta al archivo en datos
                ruta_json = os.path.join(project_dir, "datos", "rectangulos.json")
            
            # Verificar si el archivo existe
            if not os.path.exists(ruta_json):
                self._mensaje("error", f'Archivo "{ruta_json}" no encontrado.')
                # Intentar buscar en el directorio de trabajo actual como fallback
                ruta_alternativa = "rectangulos.json"
                if os.path.exists(ruta_alternativa):
                    self._mensaje("info", f'Usando archivo alternativo: {ruta_alternativa}')
                    ruta_json = ruta_alternativa
                else:
                    return None
            
            # Leer y cargar el JSON
            with open(ruta_json, "r", encoding='utf-8') as archivo:
                coords = json.load(archivo)
            
            # Verificar que existe la clave para el NIF
            if nif not in coords:
                self._mensaje("error", f'El archivo "{ruta_json}" no contiene datos para la empresa con NIF "{nif}"')
                # Mostrar las claves disponibles para facilitar la depuración
                claves_disponibles = list(coords.keys())
                if claves_disponibles:
                    self._mensaje("info", f"NIFs disponibles en el archivo: {', '.join(claves_disponibles)}")
                return None
            
            rectangles = coords[nif]
            self._mensaje("info", f"Rectángulos cargados correctamente para NIF: {nif}")
            return rectangles
            
        except FileNotFoundError:
            self._mensaje("error", f'Archivo "{ruta_json}" no encontrado.')
        except json.JSONDecodeError as e:
            self._mensaje("error", f'El archivo "{ruta_json}" tiene un formato JSON inválido: {str(e)}')
        except KeyError as e:
            self._mensaje("error", f'Error de clave en el JSON: {str(e)}')
        except Exception as e:
            self._mensaje("error", f'Error inesperado al cargar rectángulos: {str(e)}')
        
        return None

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
            # imagen = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_COLOR)

            # 1. Decodificar la imagen en escala de grises
            imagen = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
            _, imagen = cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # 2. Suavizado suave (filtro de mediana) para el ruido granular
            # Usamos un kernel de 3x3, el mínimo para no difuminar demasiado.
            # imagen = cv2.medianBlur(imagen, 3)

            # 3. Umbral Adaptativo: Para binarizar la imagen y manejar sombras
            # Este paso ya lo tenías, y es correcto.
            # imagen = cv2.adaptiveThreshold(imagen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            #                             cv2.THRESH_BINARY, 11, 2)

            # 4. Apertura Morfológica: LA SOLUCIÓN AL RUIDO PUNCTUAL
            # - Creamos un pequeño kernel de 2x2. Si el ruido es mayor, prueba 3x3.
            # kernel = np.ones((2,2), np.uint8)

            # - Aplicamos la Apertura. Esto:
            #   a) Erode la imagen (elimina los puntos negros pequeños).
            #   b) Dilata la imagen (restaura el grosor de las letras).
            # imagen = cv2.morphologyEx(imagen, cv2.MORPH_OPEN, kernel)

            # (Opcional) Si las letras quedan muy finas, puedes engrosarlas 
            # imagen = cv2.erode(imagen, kernel, iterations=1)

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