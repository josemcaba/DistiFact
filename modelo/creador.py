# modelo/creador_rectangulos.py
import os
import json
import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import pytesseract
from screeninfo import get_monitors
from typing import Dict, Any, Tuple, Optional

class CreadorRectangulos:
    def __init__(self, controlador):
        self.controlador = controlador
        self.rectangles = {}
        self.rectangle_counter = 1
        self.drawing = False
        self.ix, self.iy = -1, -1
        self.img = None
        self.window_name = "Crear Rectángulos"
        
        # Configuración de Tesseract (ajustar según sea necesario)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def _mensaje(self, tipo: str, mensaje: str):
        """Envía un mensaje a través del controlador"""
        if self.controlador and hasattr(self.controlador, '_mensaje_callback'):
            self.controlador._mensaje_callback(tipo, mensaje)
        else:
            print(f"[{tipo}] {mensaje}")

    def _cargar_json_rectangulos(self, ruta_json: str) -> Dict:
        """Carga el archivo JSON de rectángulos existente"""
        try:
            if os.path.exists(ruta_json):
                with open(ruta_json, "r", encoding='utf-8') as file_json:
                    return json.load(file_json)
            return {}
        except Exception as e:
            self._mensaje("error", f"Error cargando JSON: {str(e)}")
            return {}

    def _detectar_orientacion(self, imagen: np.ndarray) -> int:
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

    def _rotar_imagen(self, imagen: np.ndarray, angulo: int) -> np.ndarray:
        """Rota la imagen según el ángulo especificado"""
        if angulo == 90:
            return cv2.rotate(imagen, cv2.ROTATE_90_CLOCKWISE)
        elif angulo == 180:
            return cv2.rotate(imagen, cv2.ROTATE_180)
        elif angulo == 270:
            return cv2.rotate(imagen, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return imagen

    def _extraer_imagen_pdf(self, pdf_path: str) -> Tuple[Optional[np.ndarray], int]:
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
                angulo = self._detectar_orientacion(imagen)
                return self._rotar_imagen(imagen, angulo), angulo
                
        except Exception as e:
            self._mensaje("error", f"Error extrayendo imagen: {str(e)}")
            return None, 0

    def _get_screen_resolution(self) -> Tuple[int, int]:
        """Obtiene la resolución de pantalla más pequeña disponible"""
        try:
            monitors = get_monitors()
            if monitors:
                min_width = min(m.width for m in monitors)
                min_height = min(m.height for m in monitors)
                return min_width, min_height
        except:
            pass
        return 1280, 720  # Resolución por defecto

    def _ajustar_tamano_ventana(self, imagen: np.ndarray, scale_factor=0.9) -> Tuple[int, int]:
        """Calcula el tamaño adecuado para mostrar la imagen"""
        screen_width, screen_height = self._get_screen_resolution()
        img_height, img_width = imagen.shape[:2]
        
        scale_width = (screen_width * scale_factor) / img_width
        scale_height = (screen_height * scale_factor) / img_height
        scale = min(scale_width, scale_height, 1.0)  # No escalar más allá del 100%
        
        return int(img_width * scale), int(img_height * scale)

    def _dibujar_rectangulo(self, event, x, y, flags, param):
        """Callback para manejar eventos del mouse"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
            self._mensaje("info", f"Click en: ({self.ix}, {self.iy})")

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                img_copy = self.img.copy()
                cv2.rectangle(img_copy, (self.ix, self.iy), (x, y), (0, 255, 0), 3)
                cv2.imshow(self.window_name, img_copy)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            fx, fy = x, y
            # Asegurar coordenadas dentro de la imagen
            fx = min(fx, self.img.shape[1])
            fy = min(fy, self.img.shape[0])
            
            # Dibujar rectángulo permanente
            cv2.rectangle(self.img, (self.ix, self.iy), (fx, fy), (255, 0, 255), 3)
            cv2.imshow(self.window_name, self.img)
            self._mensaje("info", f"Rectángulo creado: ({self.ix}, {self.iy}) a ({fx}, {fy})")
            
            # Guardar coordenadas
            key = f"rectangulo_{self.rectangle_counter}"
            self.rectangles[key] = {
                "x1": self.ix, 
                "y1": self.iy, 
                "x2": fx, 
                "y2": fy,
                "tesseract": "-l spa --psm 6 --oem 3 -c tessedit_char_blacklist=\"\\!|=@#$£&*{}[]:;\" -c preserve_interword_spaces=1"
            }
            self.rectangle_counter += 1

    def crear(self, ruta_pdf: str, empresa_dict: Dict[str, Any]) -> bool:
        """Método principal para crear rectángulos (sobrescribe configuración existente)"""
        try:
            # 1. Verificar entrada
            if not os.path.isfile(ruta_pdf):
                self._mensaje("error", f"Archivo no encontrado: {ruta_pdf}")
                return False
                
            if not empresa_dict or "nif" not in empresa_dict:
                self._mensaje("error", "Datos de empresa inválidos")
                return False
                
            nif_empresa = empresa_dict["nif"]
            
            # 2. Inicializar estado (siempre comenzamos desde cero)
            self.rectangles = {}
            self.rectangle_counter = 1
            self.drawing = False
            
            # 3. Cargar configuración existente
            ruta_json = "rectangulos.json"
            dict_json = self._cargar_json_rectangulos(ruta_json)
            
            # 4. Extraer imagen del PDF
            self.img, angulo = self._extraer_imagen_pdf(ruta_pdf)
            if self.img is None:
                return False
                
            # 5. Configurar ventana de OpenCV
            w, h = self._ajustar_tamano_ventana(self.img)
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(self.window_name, w, h)
            cv2.imshow(self.window_name, self.img)
            cv2.setMouseCallback(self.window_name, self._dibujar_rectangulo)
            
            # 6. Mantener ventana abierta
            self._mensaje("info", "Dibuje rectángulos y presione ESC al terminar")
            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # Tecla ESC
                    break
                    
            # 7. Guardar resultados (sobrescribir completamente)
            cv2.destroyAllWindows()
            
            # Crear nueva configuración (elimina cualquier configuración anterior)
            nueva_configuracion = {
                "angulo": angulo
            }
            
            # Añadir todos los rectángulos creados
            for key, rect in self.rectangles.items():
                nueva_configuracion[key] = rect
            
            # Sobrescribir configuración para esta empresa
            dict_json[nif_empresa] = nueva_configuracion
            
            with open(ruta_json, "w", encoding='utf-8') as f:
                json.dump(dict_json, f, indent=4, ensure_ascii=False)
                
            self._mensaje("success", f"Configuración actualizada para {empresa_dict.get('nombre', nif_empresa)}")
            self._mensaje("info", f"Rectángulos guardados: {len(self.rectangles)}")
            return True
            
        except Exception as e:
            self._mensaje("error", f"Error inesperado: {str(e)}")
            return False

    def set_mensaje_callback(self, callback):
        """Establece el callback para mensajes"""
        self._mensaje_callback = callback
    