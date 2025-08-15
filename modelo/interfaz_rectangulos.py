# modelo/interfaz_rectangulos.py
import cv2
from screeninfo import get_monitors
from typing import Tuple, Dict, Callable, Any
import numpy as np

class InterfazRectangulos:
    def __init__(self, mensaje_callback=None):
        self._mensaje_callback = mensaje_callback
        self.window_name = "Crear Rectangulos"
        self.drawing = False
        self.ix, self.iy = -1, -1
    
    def _mensaje(self, tipo: str, mensaje: str):
        if self._mensaje_callback:
            self._mensaje_callback(tipo, mensaje)
        else:
            print(f"[{tipo}] {mensaje}")

    def get_screen_resolution(self) -> Tuple[int, int]:
        """Obtiene la resolución de pantalla más pequeña disponible"""
        try:
            monitors = get_monitors()
            if monitors:
                min_width = min(m.width for m in monitors)
                min_height = min(m.height for m in monitors)
                return min_width, min_height
        except:
            pass
        return 1280, 720

    def ajustar_tamano_ventana(self, imagen: np.ndarray, scale_factor=0.9) -> Tuple[int, int]:
        """Calcula el tamaño adecuado para mostrar la imagen"""
        screen_width, screen_height = self.get_screen_resolution()
        img_height, img_width = imagen.shape[:2]
        
        scale_width = (screen_width * scale_factor) / img_width
        scale_height = (screen_height * scale_factor) / img_height
        scale = min(scale_width, scale_height, 1.0)
        
        return int(img_width * scale), int(img_height * scale)

    def crear_callback_dibujo(self, img: np.ndarray, rectangles: Dict, rectangle_counter: int) -> Callable:
        """Crea la función de callback para el dibujo de rectángulos"""
        def dibujar_rectangulo(event, x, y, flags, param):
            nonlocal rectangle_counter
            
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.ix, self.iy = x, y
                self._mensaje("info", f"Click en: ({self.ix}, {self.iy})")

            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing:
                    img_copy = img.copy()
                    cv2.rectangle(img_copy, (self.ix, self.iy), (x, y), (0, 255, 0), 3)
                    cv2.imshow(self.window_name, img_copy)

            elif event == cv2.EVENT_LBUTTONUP:
                self.drawing = False
                fx, fy = x, y
                # Asegurar coordenadas dentro de la imagen
                fx = min(fx, img.shape[1])
                fy = min(fy, img.shape[0])
                
                # Dibujar rectángulo permanente
                cv2.rectangle(img, (self.ix, self.iy), (fx, fy), (255, 0, 255), 3)
                cv2.imshow(self.window_name, img)
                self._mensaje("info", f"Rectángulo creado: ({self.ix}, {self.iy}) a ({fx}, {fy})")
                
                # Guardar coordenadas
                key = f"rectangulo_{rectangle_counter}"
                rectangles[key] = {
                    "x1": self.ix, 
                    "y1": self.iy, 
                    "x2": fx, 
                    "y2": fy,
                    "tesseract": "-l spa --psm 6 --oem 3 -c tessedit_char_blacklist=\"\\!|=@#$£&*{}[]:;\" -c preserve_interword_spaces=1"
                }
                rectangle_counter += 1
        
        return dibujar_rectangulo

    def mostrar_ventana_imagen(self, img: np.ndarray, callback_mouse: Callable):
        """Muestra la imagen en una ventana redimensionada"""
        w, h = self.ajustar_tamano_ventana(img)
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, w, h)
        cv2.imshow(self.window_name, img)
        cv2.setMouseCallback(self.window_name, callback_mouse)

    def set_mensaje_callback(self, callback):
        self._mensaje_callback = callback