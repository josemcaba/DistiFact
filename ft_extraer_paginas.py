
import pdfplumber

def tipo_texto(pdf_path):
    paginas = []
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            paginas.append(texto)
    return paginas

def tipo_imagen(pdf_path):
    pass


