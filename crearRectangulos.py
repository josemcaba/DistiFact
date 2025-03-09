import fitz  # PyMuPDF
import numpy as np
import json
import cv2
from ft_seleccionarEmpresa import seleccionarEmpresa
import ft_comunes_img as fci
from sys import exit

# Variables globales
windowName = "Factura"
drawing = False
rectangle_counter = 1
rectangles = {}

def cargar_json (ruta_json):
	try:
		with open(ruta_json, "r", encoding='utf-8') as file_json:
			dict_json = json.load(file_json)
			return dict_json
	except FileNotFoundError:
		print(f'\n❌ Error: Archivo "{ruta_json}" no encontrado.')
		return
	except (json.JSONDecodeError):
		print(f'\n❌ Error: El archivo "{ruta_json}" tiene un formato inválido.')
		return

def extract_first_image_from_pdf(ruta_pdf):
    file_pdf = fitz.open(ruta_pdf)
    if not file_pdf:
        return None
    img = file_pdf.get_page_images(0)[0]
    xref = img[0]
    base_image = file_pdf.extract_image(xref)
    image_bytes = base_image["image"]
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    
	# Verificar la orientación de la imagen y rotarla si es necesario
    if image.shape[0] < image.shape[1]:  # Si la altura es menor que el ancho, rotar 90 grados
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return image

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, fx, fy, drawing, rectangles, rectangle_counter

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        print(f"Click en: ({ix}, {iy})")

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
        print(f"Rectángulo desde: ({ix}, {iy}) hasta ({fx}, {fy})")

        # Guardar las coordenadas del rectángulo en el diccionario con una clave única
        key = f"rectangulo_{rectangle_counter}"
        rectangles[key] = {"x1": ix, "y1": iy, "x2": fx, "y2": fy}
        rectangles[key]["tesseract"] = "r'--psm 6'"
        rectangle_counter += 1  # Incrementar el contador


empresa, ruta_PDF = seleccionarEmpresa("empresas.json")
if not(empresa and ruta_PDF):
	print("\n👋 Saliendo del programa...\n")
	exit()

dict_json = cargar_json("rectangulos.json")
if not (dict_json and dict_json[empresa["nif"]]):
    print("\nEsa empresa NO tiene sus rectángulos definidos")
    exit()

if empresa["nif"] in dict_json:
    print("\nEsa empresa ya tiene sus rectángulos definidos")
    exit()
dict_json[empresa["nif"]] = {}
rectangles = dict_json[empresa["nif"]]

# Extraer la imagen del PDF
img = extract_first_image_from_pdf(ruta_PDF)
if img is None:
	print("No se encontró ninguna imagen en el PDF.")
	exit()

# Mostrar la imagen en una ventana
cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
fci.adjust_window_size(windowName, img)
cv2.setMouseCallback(windowName, draw_rectangle)
cv2.imshow(windowName, img)
cv2.waitKey(0)
cv2.destroyAllWindows()

with open("rectangulos.json", "w", encoding='utf-8') as f:
    json.dump(dict_json, f, indent=4)
print(f"Coordenadas guardadas en \"rectangulos.json\"")

exit()