import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

print(pytesseract.get_languages())

img = Image.open('Pagina_1.jpg')
text = pytesseract.image_to_string(img)
print(text)