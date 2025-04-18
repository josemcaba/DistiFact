from importlib import import_module    # Para importar un modulo almacenado en una variable
import pdfplumber
import ft_imagenes as fci
import fitz  # PyMuPDF
import sys
from ft_mensajes_POO import msg

def procesarPaginasPDF_tipoImagen(pdf_path, identificador, nif):
    rectangulos = fci.cargar_rectangulos_json(nif, ruta_json="rectangulos.json")   # Cargamos solo la informacion de la empresa
    if not rectangulos:
        return
    angulo = rectangulos["angulo"]
    paginas = []
    paginas_descartadas = []
    with fitz.open(pdf_path) as pdf_doc:
        total_paginas = len(pdf_doc)
        for n_pag in range(total_paginas):
            imagen_pag = fci.extraer_imagen_de_la_pagina(pdf_doc, n_pag, angulo)
            imagenes = fci.extraer_imagenes_de_los_rectangulos(imagen_pag, rectangulos)
            texto = fci.extraer_texto_de_las_imagenes(imagenes, verRectangulos=False)
            flush_page(n_pag)
            if texto:
                if identificador in texto:
                    paginas.append([n_pag+1, texto])
                else:
                    paginas_descartadas.append(str(n_pag+1))
    msg.info(f'\nProcesadas {total_paginas} páginas')
    if len(paginas_descartadas):
        msg.info(f"Páginas descartadas: {' - '.join(paginas_descartadas)}")
    return (paginas)
    
def procesarPaginasPDF_tipoTexto(pdf_path, identificador):
    paginas = []
    paginas_descartadas = []
    with pdfplumber.open(pdf_path) as pdf:
        for n_pag, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text()
            flush_page(n_pag)
            if texto:
                if identificador in texto:
                    paginas.append([n_pag, texto])
                else:
                    paginas_descartadas.append(str(n_pag))
    msg.info(f'\nProcesadas {n_pag} páginas')
    if len(paginas_descartadas):
        msg.info(f"Páginas descartadas: {' - '.join(paginas_descartadas)}")
    return (paginas)

def procesarFacturas(path, empresa):
    try:
        # Carga el modulo de funciones correspondientes a la empresa seleccionada
        fe = import_module(empresa["funciones"][:-3])
    except:
        msg.error(f'No existe el modulo "{empresa["funciones"]}"')
        return
    if empresa["tipoPDF"] == "texto":
        paginas = procesarPaginasPDF_tipoTexto(path, fe.identificador)
    elif empresa["tipoPDF"] == "imagen":
        paginas = procesarPaginasPDF_tipoImagen(path, fe.identificador, empresa["nif"])
    else:
        msg.error(f'PDF tipo "{empresa["tipoPDF"]}" no es válido')
        return
    if not paginas:
        return
    facturas = []
    for pagina in paginas:
        factura = fe.extraerDatosFactura(pagina, empresa)
        if factura:
            facturas.append(factura)
    if not facturas:
        msg.error(f'El PDF "{path}" no contine facturas')
        return
    return facturas

def spinner(indice):
    simbolos = ["-", "\\", "|", "/"]  # Secuencia del spinner
    
    indice = indice % 4
    sys.stdout.write("\b\b\b\b" + simbolos[indice])  # Mueve el cursor atrás y sobrescribe solo el spinner
    sys.stdout.flush()  # Asegura que se imprima inmediatamente

def flush_page(num_page):
    sys.stdout.write(f'\b\b\b\b{num_page + 1} ')  # Mueve el cursor atrás y sobrescribe solo el spinner
    sys.stdout.flush()  # Asegura que se imprima inmediatamente
