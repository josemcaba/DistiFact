import cv2
import json
import numpy as np
import fitz  # PyMuPDF
import sys

# Función para extraer la imagen del PDF
def extract_image_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

            # Verificar la orientación de la imagen y rotarla si es necesario
            if image.shape[0] < image.shape[1]:  # Si la altura es menor que el ancho, rotar 90 grados
                image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            return image
    return None

# Función para cargar las coordenadas desde un archivo JSON
def load_rectangles_from_json(json_path):
    with open(json_path, "r") as f:
        rectangles = json.load(f)
    return rectangles

# Función para mostrar los trozos de imagen según las coordenadas del JSON
def show_cropped_images(pdf_path, json_path):
    # Extraer la imagen del PDF
    image = extract_image_from_pdf(pdf_path)
    if image is None:
        print("No se encontró ninguna imagen en el PDF.")
        return

    # Cargar las coordenadas desde el archivo JSON
    rectangles = load_rectangles_from_json(json_path)

    # Recortar y mostrar cada trozo de imagen
    for key, coords in rectangles.items():
        x1, y1 = coords["x1"], coords["y1"]
        x2, y2 = coords["x2"], coords["y2"]
        cropped_image = image[y1:y2, x1:x2]  # Recortar la región de la imagen

        # Mostrar la imagen recortada en una ventana
        cv2.imshow(key, cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Función principal
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python mostrar_trozos.py <archivo_pdf> <archivo_json>")
    else:
        pdf_path = sys.argv[1]
        json_path = sys.argv[2]
        show_cropped_images(pdf_path, json_path)