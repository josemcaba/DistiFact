import fitz  # Módulo PyMuPDF
import json
import cv2
import ft_imagenes as fti
from ft_seleccionarEmpresa import seleccionarEmpresa
from ft_mostrar_imagen import mostrar_imagen
from PIL import Image  # Para convertir imágenes a formato compatible con pytesseract
from sys import exit
from ft_mensajes_POO import msg
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Variables globales
windowName = "Factura"
drawing = False
rectangle_counter = 1
rectangles = {}

def cargar_json_completo(ruta_json):
	try:
		with open(ruta_json, "r", encoding='utf-8') as file_json:
			dict_json = json.load(file_json)
			return dict_json
	except FileNotFoundError:
		msg.error(f'Archivo "{ruta_json}" no encontrado.')
		return
	except (json.JSONDecodeError):
		msg.error(f'El archivo "{ruta_json}" tiene un formato inválido.')
		return

def detectar_orientacion(imagen):
    """
    Detecta la orientación de la imagen usando Tesseract OSD.
    Devuelve el ángulo de rotación necesario para corregirla.
    """
    try:
        # Convertir la imagen a formato PIL porque Tesseract lo requiere
        pil_image = Image.fromarray(imagen)

        # Obtener la información de orientación de Tesseract
        osd = pytesseract.image_to_osd(pil_image)
        
        # Extraer el ángulo de rotación
        for line in osd.split("\n"):
            if "Rotate" in line:
                angulo = int(line.split(":")[-1].strip())
                return angulo
        
    except Exception as e:
        msg.error(f"No se pudo detectar la orientación ({e})")
    
    return 0  # Si hay un error, asumimos que no hay rotación necesaria


def extract_first_image_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf_doc:
        imagen = fti.extraer_imagen_de_la_pagina(pdf_doc, 0)
    
    # Detectar la orientación de la imagen
    angulo = detectar_orientacion(imagen)

    # Rotar la imagen según el ángulo detectado
    imagen = fti.rotar_imagen(imagen, angulo)

    return imagen, angulo

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, fx, fy, drawing, rectangles, rectangle_counter

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        msg.info(f"Click en: ({ix}, {iy})")

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 5)  # Grosor del borde aumentado
            cv2.imshow(windowName, img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        fx, fy = x, y
        fx=img.shape[1] if (fx > img.shape[1]) else fx
        fy=img.shape[0] if (fy > img.shape[0]) else fy
        cv2.rectangle(img, (ix, iy), (fx, fy), (255, 0, 255), 5)  # Grosor del borde aumentado
        cv2.imshow(windowName, img)
        msg.info(f"Rectángulo desde: ({ix}, {iy}) hasta ({fx}, {fy})")

        # Guardar las coordenadas del rectángulo en el diccionario con una clave única
        key = f"rectangulo_{rectangle_counter}"
        rectangles[key] = {"x1": ix, "y1": iy, "x2": fx, "y2": fy}
        rectangles[key]["tesseract"] = "-l spa --psm 6 --oem 3 -c tessedit_char_blacklist=\"\\!|=@#$£&*{}[]:;\" -c preserve_interword_spaces=1"
        rectangle_counter += 1  # Incrementar el contador

empresa, ruta_PDF = seleccionarEmpresa("empresas.json")
if not(empresa and ruta_PDF):
	msg.salida()
	exit()

dict_json = cargar_json_completo("rectangulos.json")
if not dict_json:
    exit()

dict_json[empresa["nif"]] = {}
rectangles = dict_json[empresa["nif"]]

img, angulo = extract_first_image_from_pdf(ruta_PDF)
if img is None:
	msg.error("No se encontró ninguna imagen en el PDF.")
	exit()

mostrar_imagen(img, windowName, draw_rectangle)
rectangles["angulo"] = angulo

with open("rectangulos.json", "w", encoding='utf-8') as f:
    json.dump(dict_json, f, indent=4)
msg.info(f"Coordenadas guardadas en \"rectangulos.json\"")

exit()
