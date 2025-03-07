from importlib import import_module    # Para importar un modulo almacenado en una variable
import pandas as pd
import pdfplumber
import pdf2image

import ft_comunes_img as fci
import fitz  # PyMuPDF
import cv2
import numpy as np


def extraerPaginasPDF_tipoImagen(pdf_path, identificador, nif):
    rectangulos = fci.cagar_rectangulos_json(nif)
    if not rectangulos:
        return
    print("\nPáginas descartadas:", end=" ")
    paginas = []
    pdf_doc = fitz.open(pdf_path)
    total_paginas = len(pdf_doc)
    for n_pag in range(total_paginas):
        texto = fci.extract_texto_form_page(pdf_doc, n_pag, rectangulos)
        if texto:
            if identificador in texto:
                paginas.append(texto)
            else:
                print(f"- {n_pag}", end=" ")
    print("-")
    return (paginas)

def extraerPaginasPDF_tipoTexto(pdf_path, identificador):
    print("\nPáginas descartadas:", end=" ")
    paginas = []
    with pdfplumber.open(pdf_path) as pdf:
        for n_pag, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text()
            if texto:
                if identificador in texto:
                    paginas.append(texto)
                else:
                    print(f"- {n_pag}", end=" ")
    print("-")
    return (paginas)

def extraerFacturas(path, empresa):
    # Carga el modulo de funciones correspondientes a la empresa seleccionada
    fe = import_module(empresa["funciones"][:-3])
    if empresa["tipoPDF"] == "texto":
        paginas = extraerPaginasPDF_tipoTexto(path, fe.identificador)
    elif empresa["tipoPDF"] == "imagen":
        paginas = extraerPaginasPDF_tipoImagen(path, fe.identificador, empresa["nif"])
    else:
        print(f'\n❌ Error: PDF tipo "{empresa["tipoPDF"]}" no es válido')
        return
    if not paginas:
        return
    facturas = []
    for pagina in paginas:
        factura = fe.extraerDatosFactura(pagina, empresa)
        if factura:
            facturas.append(factura)
    if not facturas:
        print(f'\n❌ El PDF "{path}" no contine facturas')
        return
    return facturas

def exportar_a_excel(facturas_correctas, facturas_con_errores, excel_path):
    """
    Exporta las facturas correctas y con errores a archivos Excel separados.
    """
    columnas = [
        "Numero Factura", "Fecha Factura", "Fecha Operacion", "Concepto",
        "Base IVA", "Tipo IVA", "Cuota IVA", 
        "Base IRPF", "Tipo IRPF", "Cuota IRPF",
        "Base R. Equiv.", "Tipo R. Equiv.", "Cuota R. Equiv.",
        "NIF", "Nombre Cliente"
    ]

    # Exportar facturas correctas
    if facturas_correctas:
        df_correctas = pd.DataFrame(facturas_correctas, columns=columnas + ["Observaciones"])
        df_correctas = df_correctas.sort_values(by=columnas[0])
        df_correctas.to_excel(excel_path.replace(".xlsx", "_correctas.xlsx"), index=False)
        print(f"Se han exportado {len(facturas_correctas)} facturas correctas.")
    else:
        print("No hay facturas correctas para exportar.")

    # Exportar facturas con errores
    if facturas_con_errores:
        df_errores = pd.DataFrame(facturas_con_errores, columns=columnas + ["Errores"])
        df_errores = df_errores.sort_values(by=columnas[0])
        df_errores.to_excel(excel_path.replace(".xlsx", "_errores.xlsx"), index=False)
        print(f"Se han exportado {len(facturas_con_errores)} facturas con errores.")
    else:
        print("No hay facturas con errores para exportar.")
    print()
