import cv2
import numpy as np
import json
from PIL import Image  # Para convertir imágenes a formato compatible con pytesseract
from ft_mostrar_imagen import mostrar_imagen
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extraer_imagen_de_la_pagina(pdf_doc, n_pag, angulo = 0):
    img = pdf_doc.get_page_images(n_pag)
    if not img:
        raise ValueError(f"No se encontraron imágenes en la página {n_pag}.")
    # Extrae la primera imagen porque asumimos que solo hay una imagen
    xref = img[0][0]
    base_imagen = pdf_doc.extract_image(xref)
    imagen_bytes = base_imagen["image"]
    imagen = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_COLOR)
    imagen = rotar_imagen(imagen, angulo)
    return (imagen)

def rotar_imagen(imagen, angulo):
    if angulo == 90:
        imagen = cv2.rotate(imagen, cv2.ROTATE_90_CLOCKWISE)
    elif angulo == 180:
        imagen = cv2.rotate(imagen, cv2.ROTATE_180)
    elif angulo == 270:
        imagen = cv2.rotate(imagen, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return imagen

def cargar_rectangulos_json(nif, ruta_json="rectangulos.json"):
    try:
        with open(ruta_json, "r", encoding='utf-8') as archivo:
            coords = json.load(archivo)
        rectangles = coords[nif]
        return rectangles
    except FileNotFoundError:
        print(f'\n❌ Error: Archivo "{ruta_json}" no encontrado.')
    except (json.JSONDecodeError):
        print(f'\n❌ Error: El archivo "{ruta_json}" tiene un formato inválido.')
    except (KeyError):
        print(f'\n❌ Error: El archivo "{ruta_json}" no contiene la empresa "{nif}"')
    return

def extraer_imagenes_de_los_rectangulos(imagen, rectangulos):
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
            print(f"Advertencia: Coordenadas {key} fuera de los límites de la imagen.")
            continue
        
        cropped_image = imagen[y1:y2, x1:x2]  # Recortar la región de la imagen
        tesseract_config = coords["tesseract"]
        imagenes.append([cropped_image, tesseract_config])
    return (imagenes)

def extraer_texto_de_las_imagenes(imagenes, verRectangulos=False):
    texto_completo = ""
    for imagen in imagenes:
        texto_imagen = extraer_texto_de_imagen(imagen[0], imagen[1], verRectangulos)
        texto_completo += f"{texto_imagen}\n"
    return (texto_completo)

def extraer_texto_de_imagen(imagen, tesseract_config, verRectangulos=False):
    # Preprocesar la imagen
    imagen = preprocesar_imagen(imagen)
    if imagen is None:
        return ""

    # Ajustar la resolución
    # processed_image = adjust_resolution(processed_image)
    
    # Convertir la imagen de OpenCV a formato PIL
    pil_image = Image.fromarray(imagen)
    # tesseract_config = "--psm 6 --oem 3 -c tessedit_char_blacklist=\"@#$&*{A}[]:;\""
    text = pytesseract.image_to_string(pil_image, config=tesseract_config)
    if verRectangulos:
        print(text)
        mostrar_imagen(imagen) 
    return text

def preprocesar_imagen(imagen):

    return imagen
    
    if len(imagen.shape) == 2:  # La imagen ya está en escala de grises (1 canal)
        gray = imagen
    elif len(imagen.shape) == 3:  # La imagen tiene 3 canales (BGR)
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    else:
        raise ValueError("La imagen no tiene un formato válido (1 o 3 canales).")

    # Aplicar umbralización (binarización)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary

    # Calcular el área de píxeles blancos para ver si hay suficiente texto en la imagen
    min_text_area=100
    text_area = cv2.countNonZero(binary)
    if text_area < min_text_area:
        print("⚠️ Advertencia: La imagen no contiene suficiente texto. Se omitirá.")
        return None

    # Aplicar un desenfoque para reducir el ruido
    blurred = cv2.GaussianBlur(binary, (5, 5), 0)

    # Opcional: Ajustar el contraste y el brillo
    alpha = 1.5  # Control de contraste (1.0 es neutral)
    beta = 0     # Control de brillo (0 es neutral)
    adjusted = cv2.convertScaleAbs(blurred, alpha=alpha, beta=beta)

    return adjusted

