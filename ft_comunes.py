import conceptos_factura as KEY
from importlib import import_module    # Para importar un modulo almacenado en una variable
import pandas as pd
import pdfplumber
import ft_imagenes as fci
import fitz  # PyMuPDF
import sys
from ft_mensajes import msg

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
            spinner(n_pag)
            imagen_pag = fci.extraer_imagen_de_la_pagina(pdf_doc, n_pag, angulo)
            imagenes = fci.extraer_imagenes_de_los_rectangulos(imagen_pag, rectangulos)
            texto = fci.extraer_texto_de_las_imagenes(imagenes, verRectangulos=False)
            if texto:
                if identificador in texto:
                    paginas.append(texto)
                else:
                    paginas_descartadas.append(n_pag)
    msg.info(f"Páginas descartadas: {paginas_descartadas}") 
    return (paginas)
    
def procesarPaginasPDF_tipoTexto(pdf_path, identificador):
    paginas = []
    paginas_descartadas = []
    with pdfplumber.open(pdf_path) as pdf:
        for n_pag, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text()
            spinner(n_pag)
            if texto:
                if identificador in texto:
                    paginas.append(texto)
                else:
                    paginas_descartadas.append(n_pag)
    msg.info(f"Páginas descartadas: {paginas_descartadas}")
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

def exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path):
    """
    Exporta las facturas correctas y con errores a archivos Excel separados.
    """
    columnas = [
        KEY.NUM_FACT, KEY.FECHA_FACT, KEY.FECHA_OPER, KEY.CONCEPTO,
        KEY.BASE_IVA, KEY.TIPO_IVA, KEY.CUOTA_IVA, 
        KEY.BASE_IRPF, KEY.TIPO_IRPF, KEY.CUOTA_IRPF,
        KEY.BASE_RE, KEY.TIPO_RE, KEY.CUOTA_RE,
        KEY.NIF, KEY.EMPRESA
    ]

    # Exportar facturas correctas
    if facturas_correctas:
        df_correctas = pd.DataFrame(facturas_correctas, columns=columnas + ["Observaciones"])
        df_correctas = df_correctas.sort_values(by=columnas[0])
        df_correctas.to_excel(excel_path.replace(".xlsx", "_correctas.xlsx"), index=False)
        msg.info(f"Se han exportado {len(facturas_correctas)} facturas correctas.")
    else:
        msg.info("No hay facturas correctas para exportar.")

    # Exportar facturas con errores
    if facturas_con_errores:
        df_errores = pd.DataFrame(facturas_con_errores, columns=columnas + ["Errores"])
        df_errores = df_errores.sort_values(by=columnas[0])
        df_errores.to_excel(excel_path.replace(".xlsx", "_errores.xlsx"), index=False)
        msg.info(f"Se han exportado {len(facturas_con_errores)} facturas con errores.")
    else:
        msg.info("No hay facturas con errores para exportar.")

def spinner(indice):
    simbolos = ["-", "/", "|", "\\"]  # Secuencia del spinner
    
    indice = indice % 4
    sys.stdout.write("\b" + simbolos[indice])  # Mueve el cursor atrás y sobrescribe solo el spinner
    sys.stdout.flush()  # Asegura que se imprima inmediatamente
