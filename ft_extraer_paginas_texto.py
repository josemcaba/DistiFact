from importlib import import_module    # Para importar un modulo almacenado en una variable
import pdfplumber
import re
import os

def extraer_paginas_texto(pdf_path):
    """
    Extrae la información de las facturas de un archivo PDF tipo texto.
    Retorna una lista de paginas en formato convertido a texto.
    """
    if not os.path.exists(pdf_path):
        print(f"El archivo {pdf_path} no existe.")
        return []

    texto_completo = ""
    separador = "<>>>>> FACTURA <<<<<>\n"
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += separador + texto + "\n"

    paginas = re.split(separador, texto_completo)

    return paginas

def registros_facturas(seccion, nombre_proveedor, nif_proveedor, extractores):
    """
    Procesa una sección de texto para extraer los datos de una factura.
    Retorna un diccionario con los datos de la factura.
    """
    if "Fecha emisión" not in seccion:
        return None

    extraer = import_module(extractores[:-3])
    datos_factura = {
        "Num. Factura": extraer.numero_factura(seccion),
        "Fecha Fact.": extraer.fecha(seccion),
        "Fecha Oper.": extraer.fecha(seccion),
        "Concepto": 700,
        "Base I.V.A.": extraer.base_iva(seccion),
        "% I.V.A.": 0,
        "Cuota I.V.A.": extraer.cuota_iva(seccion),
        "Base I.R.P.F.": extraer.base_iva(seccion),
        "% I.R.P.F.": 0,
        "Cuota I.R.P.F.": 0,
        "Base R. Equiv.": extraer.base_iva(seccion),
        "% R. Equiv.": 0,
        "Cuota R. Equiv.": 0,
        "NIF/DNI": extraer.nif_cliente(seccion, nif_proveedor),
        "Nombre": extraer.nombre_cliente(seccion, nombre_proveedor),
        "Total Factura": extraer.total_factura(seccion)
    }

    # Calcular % I.V.A.
    base_valor = datos_factura["Base I.V.A."]
    iva_valor = datos_factura["Cuota I.V.A."]
    datos_factura["% I.V.A."] = int(round((iva_valor / base_valor) * 100)) if base_valor else 0

    return datos_factura