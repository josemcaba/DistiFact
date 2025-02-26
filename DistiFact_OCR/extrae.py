import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import re

# Configura la ruta de Tesseract si no está en el PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Función para extraer datos de las facturas
def extract_invoice_data(text):
    print(text)
    invoices = []
    invoice_pattern = re.compile(
        r'Número\s*(\d{2}/\d{4}).*?Fecha\s*(\d{2}/\d{2}/\d{4}).*?Descripcion\s*(.*?)\s*LECTURA ANTERIOR.*?Base Imponible\s*([\d,.]+).*?% IVA\s*(\d+).*?Cuota IVA\s*([\d,.]+).*?TOTAL\s*([\d,.]+)',
        re.DOTALL
    )
    matches = invoice_pattern.findall(text)
    for match in matches:
        invoice = {
            "Num. Factura": match[0].strip(),
            "Fecha Fact.": match[1].strip(),
            "Fecha Oper.": "",
            "Concepto": match[2].strip(),
            "Base I.V.A.": float(match[3].replace(',', '').strip()),
            "% I.V.A.": int(match[4].strip()),
            "Cuota I.V.A.": float(match[5].replace(',', '').strip()),
            "Base I.R.P.F.": "",
            "% I.R.P.F.": "",
            "Cuota I.R.P.F.": "",
            "Base R. Equiv.": "",
            "% R. Equiv.": "",
            "Cuota R. Equiv.": "",
            "NIF/DNI": "33.360.360-X",
            "Nombre del cliente": "IGNACIO IBANEZ PACHECO"
        }
        invoices.append(invoice)
    return invoices

# Función para extraer texto de un PDF con imágenes usando OCR
def extract_text_from_pdf(pdf_path):
    # Convertir el PDF en una lista de imágenes
    images = convert_from_path(pdf_path)

    # Extraer texto de cada imagen usando Tesseract
    full_text = ""
    for image in images:
        text = pytesseract.image_to_string(image, lang='spa')  # 'spa' para español
        full_text += text + "\n"

    return full_text

# Ruta del archivo PDF
pdf_file_path = "facturas.pdf"

# Extraer texto del PDF usando OCR
pdf_text = extract_text_from_pdf(pdf_file_path)

# Extraer datos de las facturas
invoices = extract_invoice_data(pdf_text)

# Crear un DataFrame con los datos
df = pd.DataFrame(invoices)

# Guardar el DataFrame en un archivo Excel
df.to_excel("facturas.xlsx", index=False)

print("Archivo Excel generado con éxito: facturas.xlsx")