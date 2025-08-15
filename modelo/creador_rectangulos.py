# modelo/creador_rectangulos.py
import os
import json
import cv2
from typing import Dict, Any
from .extractor_imagenes import ExtractorImagenes
from .interfaz_rectangulos import InterfazRectangulos
import pytesseract
import fitz  # PyMuPDF

class CreadorRectangulos:
    def __init__(self, controlador):
        self.controlador = controlador
        self.extractor = ExtractorImagenes()
        self.interfaz = InterfazRectangulos()
        self.rectangles = {}
        self.rectangle_counter = 1
        self.img = None
        
        # Configuración de Tesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def _mensaje(self, tipo: str, mensaje: str):
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

    def crear(self, ruta_pdf: str, empresa_dict: Dict[str, Any]) -> bool:
        """Método principal para crear rectángulos (sobrescribe configuración existente)"""
        try:
            # 1. Configurar callbacks
            self.manejador_imagenes.set_mensaje_callback(self._mensaje)
            self.interfaz.set_mensaje_callback(self._mensaje)
            
            # 2. Verificar entrada
            if not empresa_dict or "nif" not in empresa_dict:
                self._mensaje("error", "Datos de empresa inválidos")
                return False
                
            nif_empresa = empresa_dict["nif"]
            
            # 3. Inicializar estado
            self.rectangles = {}
            self.rectangle_counter = 1
            
            # 4. Cargar configuración existente
            ruta_json = "rectangulos.json"
            dict_json = self._cargar_json_rectangulos(ruta_json)
            
            # 5. Extraer imagen del PDF
            with fitz.open(ruta_pdf) as pdf_doc:
                self.img, angulo = self.extractor.extraer_imagen_de_pdf(pdf_doc)
                if self.img is None:
                    return False
                
            # 6. Configurar interfaz
            callback_dibujo = self.interfaz.crear_callback_dibujo(
                self.img, self.rectangles, self.rectangle_counter
            )
            self.interfaz.mostrar_ventana_imagen(self.img, callback_dibujo)
            
            # 7. Mantener ventana abierta
            self._mensaje("info", "Dibuje rectángulos y presione ESC al terminar")
            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # Tecla ESC
                    break
                    
            # 8. Guardar resultados
            cv2.destroyAllWindows()
            
            # Crear nueva configuración (sobrescribe completamente)
            nueva_configuracion = {"angulo": angulo}
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