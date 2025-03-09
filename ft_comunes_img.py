import fitz  # Módulo PyMuPDF
import cv2
import numpy as np
import json
from PIL import Image  # Para convertir imágenes a formato compatible con pytesseract
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_first_image_from_pdf(pdf_path):
    pdf_doc = fitz.open(pdf_path)
    imagen = extraer_imagen_de_la_pagina(pdf_doc, 0)
    return imagen

def save_rectangles_to_json(json_path, nif, rectangles):
    coords = {nif: rectangles}
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(coords, f, indent=4)
    print(f"Coordenadas guardadas en {json_path}")

def cagar_rectangulos_json(nif):
    ruta_json = "rectangulos.json"
    try:
        with open(ruta_json, "r", encoding='utf-8') as archivo:
            coords = json.load(archivo)

        rectangles = coords[nif]
        return rectangles
    
    except FileNotFoundError:
        print(f'\n❌ Error: Archivo "{ruta_json}" no encontrado.')
        return
    except (json.JSONDecodeError):
        print(f'\n❌ Error: El archivo "{ruta_json}" tiene un formato inválido.')
        return
    except (KeyError):
        print(f'\n❌ Error: El archivo "{ruta_json}" no contiene la empresa "{nif}"')
        return

def extraer_imagen_de_la_pagina(pdf_doc, n_pag):
    img = pdf_doc.get_page_images(n_pag)[0]
    xref = img[0]
    base_imagen = pdf_doc.extract_image(xref)
    imagen_bytes = base_imagen["image"]
    imagen = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_COLOR)
    # Verificar la orientación de la imagen y rotarla si es necesario
    if imagen.shape[0] < imagen.shape[1]:  # Si la altura es menor que el ancho, rotar 90 grados
        imagen = cv2.rotate(imagen, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return (imagen)

def extraer_imagenes_de_los_rectangulos(imagen, rectangulos):
    imagenes = []
    # Recortar y mostrar cada trozo de imagen según las coordenadas del JSON
    for key, coords in rectangulos.items():  # OJO: ¿podemos eliminar la variable key
        x1, y1 = coords["x1"], coords["y1"]
        x2, y2 = coords["x2"], coords["y2"]
        cropped_image = imagen[y1:y2, x1:x2]  # Recortar la región de la imagen
        tesseeract_config = coords["tesseract"]   
        imagenes.append([cropped_image, tesseeract_config])
    return (imagenes)

def extraer_texto_de_las_imagenes(imagenes):
    texto_completo = ""
    for imagen in imagenes:
        texto_imagen = extraer_texto_de_imagen(imagen[0], imagen[1])
        texto_completo += f"{texto_imagen}\n"
    return (texto_completo)

def extraer_texto_de_imagen(imagen, tesseeract_config):
    # Preprocesar la imagen
    imagen = preprocesar_imagen(imagen)

    # Ajustar la resolución
    # processed_image = adjust_resolution(processed_image)
    
    # Verificar si la imagen tiene suficiente texto
    if not has_enough_text(imagen):
        return ""  # Si no hay suficiente texto, devolver una cadena vacía
    
    # Convertir la imagen de OpenCV a formato PIL
    pil_image = Image.fromarray(imagen)
    
    # Aplicar OCR con configuración personalizada
    # custom_config = r'--psm 6 -l spa'  # Modo 11 para texto disperso, idioma español
    text = pytesseract.image_to_string(pil_image, config=tesseeract_config)

    return text

def preprocesar_imagen(imagen):
    # Verificar el número de canales de la imagen
    if len(imagen.shape) == 2:  # La imagen ya está en escala de grises (1 canal)
        gray = imagen
    elif len(imagen.shape) == 3:  # La imagen tiene 3 canales (BGR)
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    else:
        raise ValueError("La imagen no tiene un formato válido (1 o 3 canales).")

    # Aplicar un desenfoque para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Aplicar umbralización (binarización)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Opcional: Ajustar el contraste y el brillo
    alpha = 1.5  # Control de contraste (1.0 es neutral)
    beta = 0     # Control de brillo (0 es neutral)
    adjusted = cv2.convertScaleAbs(binary, alpha=alpha, beta=beta)

    return adjusted

def has_enough_text(image, min_text_area=100):
    # Verificar el número de canales de la imagen
    if len(image.shape) == 2:  # La imagen ya está en escala de grises (1 canal)
        gray = image
    elif len(image.shape) == 3:  # La imagen tiene 3 canales (BGR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        raise ValueError("La imagen no tiene un formato válido (1 o 3 canales).")

    # Aplicar umbralización (binarización)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Calcular el área de píxeles blancos (texto)
    text_area = cv2.countNonZero(binary)
    return text_area > min_text_area