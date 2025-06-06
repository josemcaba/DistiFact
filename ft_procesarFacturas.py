from importlib import import_module    # Para importar un modulo almacenado en una variable
import pdfplumber
import ft_imagenes as fci
import fitz  # PyMuPDF
import sys
from ft_mensajes_POO import msg
import openpyxl

def procesarPaginas_tipo_PDFImagen(pdf_path, identificador, nif):
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
 
def procesarPaginas_tipo_PDFTexto(pdf_path, identificador):
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
            else:
                paginas_descartadas.append(str(n_pag))
    msg.info(f'\nProcesadas {n_pag} páginas')
    if len(paginas_descartadas):
        msg.info(f"Páginas descartadas: {' - '.join(paginas_descartadas)}")
    return (paginas)

def procesarPaginas_tipo_Excel(excel_path, identificador, nif):
    # Cargar el libro de trabajo
    libro = openpyxl.load_workbook(excel_path, data_only=True)
    
    # Seleccionar la primera hoja
    hoja = libro.active  

    filas = []
    contador = 2  # Inicializamos el contador
    
    # Iterar sobre todas las filas con contenido
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        # Filtrar filas completamente vacías (todas las celdas son None)
        if any(celda is not None for celda in fila):
            # Crear una nueva lista que comience con el contador
            fila = [contador] + list(fila)
            filas.append(fila)
            contador += 1  # Incrementar el contador
    
    return filas

def procesarFacturas(path, empresa):
    try:
        # Carga el modulo de funciones extractoras correspondientes a la empresa seleccionada
        fe = import_module(empresa["funciones"][:-3])
    except:
        msg.error(f'No existe el modulo "{empresa["funciones"]}"')
        return
    if empresa["tipo"] == "PDFtexto":
        paginas = procesarPaginas_tipo_PDFTexto(path, fe.identificador)
    elif empresa["tipo"] == "PDFimagen":
        paginas = procesarPaginas_tipo_PDFImagen(path, fe.identificador, empresa["nif"])
    elif empresa["tipo"] == "excel":
        paginas = procesarPaginas_tipo_Excel(path, fe.identificador, empresa["nif"])
    else:
        msg.error(f'PDF tipo "{empresa["tipo"]}" no es válido')
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
