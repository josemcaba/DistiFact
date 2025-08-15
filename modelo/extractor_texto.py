"""
OCR
Módulo que contiene la clase para el reconocimiento de texto en imágenes
"""
from PIL import Image  # Para convertir imágenes a formato compatible con pytesseract
import pytesseract


class ExtractorTexto:
	def __init__(self):
		pass

	def extraer_texto_de_las_imagenes(self, imagenes, printTexto=False):
		texto_completo = ""
		for imagen in imagenes:
			texto_imagen = self.extraer_texto_de_imagen(imagen[0], imagen[1], printTexto)
			texto_completo += f"{texto_imagen}\n"
		return (texto_completo)

	def extraer_texto_de_imagen(self, imagen, tesseract_config, printTexto=False):
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
		if printTexto:
			print(text)
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

		import cv2
		import numpy as np
		import imutils

		def display(wn, x, cvImg):
			#cvImg=cv2.resize(cvImg, (566, 800))
			cvImg = imutils.resize(cvImg, width=575)
			#cv2.namedWindow(wn, cv2.WINDOW_NORMAL)
			cv2.imshow(wn,cvImg)
			cv2.moveWindow(wn, x, 0)

		# Calculate skew angle of an image
		def getSkewAngle(cvImage) -> float:
			# Prep image, copy, convert to gray scale, blur, and threshold
			newImage = cvImage.copy()
			gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
			blur = cv2.GaussianBlur(gray, (9, 9), 0)
			thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

			# Apply dilate to merge text into meaningful lines/paragraphs.
			# Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
			# But use smaller kernel on Y axis to separate between different blocks of text
			kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
			dilate = cv2.dilate(thresh, kernel, iterations=5)

			# Find all contours
			contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			contours = sorted(contours, key = cv2.contourArea, reverse = True)

			# Find largest contour and surround in min area box
			largestContour = contours[0]
			minAreaRect = cv2.minAreaRect(largestContour)

			# Determine the angle. Convert it to the value that was originally used to obtain skewed image
			angle = minAreaRect[-1]
			if angle < -45:
				angle = 90 + angle
			return -1.0 * angle

		# Rotate the image around its center
		def rotateImage(cvImage, angle: float):
			newImage = cvImage.copy()
			(h, w) = newImage.shape[:2]
			center = (w // 2, h // 2)
			M = cv2.getRotationMatrix2D(center, angle, 1.0)
			newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
			return newImage

		# Deskew image
		def deskew(cvImage):
			angle = getSkewAngle(cvImage)
			print(angle)
			return rotateImage(cvImage, -1.0 * angle)

		def noise_removal(cvImage):
			kernel = np.ones((1,1), np.uint8)
			image = cv2.dilate(cvImage, kernel, iterations=1)
			kernel = np.ones((1,1), np.uint8)    
			image = cv2.erode(image, kernel, iterations=1)  
			image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
			image = cv2.medianBlur(image, 3)
			return (image)  
