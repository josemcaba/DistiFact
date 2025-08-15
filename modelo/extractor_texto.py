"""
OCR
Módulo que contiene la clase para el reconocimiento de texto en imágenes
"""
from PIL import Image  # Para convertir imágenes a formato compatible con pytesseract
import pytesseract
from .extractor_imagenes import ManejadorImagenes

class ExtractorTexto:
	def __init__(self):
		self.manejador_imagenes = ManejadorImagenes()

	def extraer_texto_de_las_imagenes(self, imagenes, verRectangulos=False):
		texto_completo = ""
		for imagen in imagenes:
			texto_imagen = self.extraer_texto_de_imagen(imagen[0], imagen[1], verRectangulos)
			texto_completo += f"{texto_imagen}\n"
		return (texto_completo)

	def extraer_texto_de_imagen(self, imagen, tesseract_config, verRectangulos=False):
		# Preprocesar la imagen
		imagen = self.preprocesar_imagen(imagen)
		if imagen is None:
			return ""

		# Ajustar la resolución
		# processed_image = adjust_resolution(processed_image)
		
		# Convertir la imagen de OpenCV a formato PIL
		pil_image = Image.fromarray(imagen)
		# tesseract_config = "--psm 6 --oem 3 -c tessedit_char_blacklist=\"@#$&*{A}[]:;\""
		text = pytesseract.image_to_string(pil_image, config=tesseract_config)
		if verRectangulos:
			msg.info(text)
			mostrar_imagen(imagen)
			self.visu
		return text

	def preprocesar_imagen(self, imagen):

		return imagen
		
		if len(imagen.shape) == 2:  # La imagen ya está en escala de grises (1 canal)
			gray = imagen
		elif len(imagen.shape) == 3:  # La imagen tiene 3 canales (BGR)
			gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
		else:
			raise ValueError("La imagen no tiene un formato válido (1 o 3 canales).")
		# return gray

		# Aplicar umbralización (binarización)
		_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		return binary

		# Aplicar un desenfoque para reducir el ruido
		blurred = cv2.GaussianBlur(binary, (5, 5), 0)
		# return blurred

		# Ajustar el contraste y el brillo
		alpha = 1.5  # Control de contraste (1.0 es neutral)
		beta = 0     # Control de brillo (0 es neutral)
		adjusted = cv2.convertScaleAbs(blurred, alpha=alpha, beta=beta)
		# return adjusted


		# Calcular el área de píxeles blancos para ver si hay suficiente texto en la imagen
		min_text_area=100
		text_area = cv2.countNonZero(binary)
		if text_area < min_text_area:
			msg.error("La imagen no contiene suficiente texto. Se omitirá.")
			return None