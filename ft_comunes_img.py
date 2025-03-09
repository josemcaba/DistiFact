import fitz  # Módulo PyMuPDF
import cv2
import numpy as np
import json
from screeninfo import get_monitors
from PIL import Image  # Para convertir imágenes a formato compatible con pytesseract
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_first_image_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    if not doc:
        return None

    img = doc.get_page_images(0)[0]
    xref = img[0]
    base_image = doc.extract_image(xref)
    image_bytes = base_image["image"]
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Verificar la orientación de la imagen y rotarla si es necesario
    if image.shape[0] < image.shape[1]:  # Si la altura es menor que el ancho, rotar 90 grados
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return image

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

def get_screen_resolution():
    width = 1440 # Resolución predeterminada si no se detecta el monitor
    height = 900 # Resolución predeterminada si no se detecta el monitor
    monitors = get_monitors()
    if monitors:
        for monitor in monitors:
            width = monitor.width if monitor.width < width else width
            height = monitor.height if monitor.height < height else height
    return width, height

def adjust_window_size(windowName, image):
    screen_width, screen_height = get_screen_resolution()
    img_height, img_width = image.shape[:2]

    # Factor de escala para imagen ajustada a la pantalla
    scale_width = screen_width / img_width
    scale_height = screen_height / img_height
    scale = 0.9 * min(scale_width, scale_height)
    scale = 1.0 if scale > 1.0 else scale

    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    
    cv2.resizeWindow(windowName, new_width, new_height)

def mostrar_imagen(image, msec=0):
    ''' Mostrar la imagen en una ventana '''
    cv2.namedWindow("Rectangulo", cv2.WINDOW_NORMAL)
    adjust_window_size("Rectangulo", image)
    cv2.imshow("Rectangulo", image)
    cv2.waitKey(msec)
    cv2.destroyAllWindows()

def extract_text_form_page(pdf_doc, pagina, rectangulos):
    texto_pag = ""
    img = pdf_doc.get_page_images(pagina)[0]
    xref = img[0]
    base_image = pdf_doc.extract_image(xref)
    image_bytes = base_image["image"]
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Verificar la orientación de la imagen y rotarla si es necesario
    if image.shape[0] < image.shape[1]:  # Si la altura es menor que el ancho, rotar 90 grados
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Recortar y mostrar cada trozo de imagen según las coordenadas del JSON
    for key, coords in rectangulos.items():
        x1, y1 = coords["x1"], coords["y1"]
        x2, y2 = coords["x2"], coords["y2"]
        cropped_image = image[y1:y2, x1:x2]  # Recortar la región de la imagen
        tesseeract_params = coords["tesseract"]
        # Aplicar OCR a la imagen recortada
        text_img = extract_text_from_image(cropped_image, tesseeract_params)

        texto_pag += f"{text_img}\n"
    
    return (texto_pag)

# Función para aplicar OCR a una imagen
def extract_text_from_image(image, custom_config):
    # Preprocesar la imagen
    processed_image = preprocess_image(image)
    processed_image = image

    # Ajustar la resolución
    # processed_image = adjust_resolution(processed_image)
    
    # Verificar si la imagen tiene suficiente texto
    if not has_enough_text(processed_image):
        return ""  # Si no hay suficiente texto, devolver una cadena vacía
    
    # Convertir la imagen de OpenCV a formato PIL
    pil_image = Image.fromarray(processed_image)
    
    # Aplicar OCR con configuración personalizada
    # custom_config = r'--psm 6 -l spa'  # Modo 11 para texto disperso, idioma español
    text = pytesseract.image_to_string(pil_image, config=custom_config)

    return text

    # Función para preprocesar la imagen antes de aplicar OCR
def preprocess_image(image):
    # Verificar el número de canales de la imagen
    if len(image.shape) == 2:  # La imagen ya está en escala de grises (1 canal)
        gray = image
    elif len(image.shape) == 3:  # La imagen tiene 3 canales (BGR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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

# Función para verificar si la imagen tiene suficiente texto
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