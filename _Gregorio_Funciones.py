import re
import ft_comunes as ft
import ft_verificadores as verificar

#
# EXTRACCION
#
def registros_factura(pagina, empresa):
    datos_factura = {
        "Num. Factura": numero_factura(pagina),
        "Fecha Fact.": fecha(pagina),
        "Fecha Oper.": fecha(pagina),
        "Concepto": 700,
        "Base I.V.A.": base_iva(pagina),
        "% I.V.A.": tipo_iva(pagina),
        "Cuota I.V.A.": cuota_iva(pagina),
        "Base I.R.P.F.": base_iva(pagina),
        "% I.R.P.F.": 0.0,
        "Cuota I.R.P.F.": 0.0,
        "Base R. Equiv.": base_iva(pagina),
        "% R. Equiv.": 0.0,
        "Cuota R. Equiv.": 0.0,
        "NIF/DNI": nif_cliente(pagina, empresa),
        "Nombre": nombre_cliente(pagina, empresa),
        "Total Factura": total_factura(pagina)
    }
    return datos_factura

# datos_factura["Num. Factura"] = regex_search(r"Número de Factura.*\s*Fact-(\d+)")

def numero_factura(pagina):
    regex = r"Número de Factura.*\s+(?:Fact-)?(\d+)"
    match = re.search(regex, pagina)
    return match.group(1) if match else None

def fecha(pagina):
    regex = r"Fecha de Facturación.*\s+(\d{2}/\d{2}/\d{4})"
    match = re.search(regex, pagina)
    return match.group(1) if match else None

def base_iva(pagina):
    regex = r"Subtotal\s+([\d.,]+)"
    match = re.search(regex, pagina)
    return match.group(1) if match else None

def tipo_iva(pagina):
    regex = r"IVA\s+\((\d+)%\)"
    match = re.search(regex, pagina)
    return match.group(1) if match else None

def cuota_iva(pagina):
    regex = r"IVA\s+\(\d+%\)\s+([\d.,]+)"
    match = re.search(regex, pagina)
    return match.group(1) if match else None

def nif_cliente(pagina, empresa):
    regex = r"\b([a-zA-Z0-9]\d{7}[a-zA-Z0-9])\b"
    match = re.findall(regex, pagina)
    # Filtrar para descartar el NIF de la empresa y seleccionar el correcto
    nif_cliente = [nif for nif in match if nif != empresa["nif"]]
    # Devuelve el primer NIF distinto o None
    return nif_cliente[0] if nif_cliente else None

def nombre_cliente(pagina, empresa):
    regex = rf"(.*?)\s+{empresa['nombre']}"
    match = re.search(regex, pagina)
    return match.group(1) if match else None

def total_factura(pagina):
    regex = r"Envío\s+Total\s+([\d.,]+)"
    match = re.search(regex, pagina)
    return match.group(1) if match else None

#
# VERIFICACION
#

def extraer_facturas_del_PDF(path, empresa):
    paginas = ft.extraer_paginas_PDF_tipo_texto(path, "Enlaza Soluciones")

    facturas = []
    for pagina in paginas:
        factura = registros_factura(pagina, empresa)
        if factura:
            facturas.append(factura)
    return facturas

def clasificar_facturas(facturas):
    """
    Clasifica las facturas en correctas y con errores.
    Retorna dos listas: facturas_correctas y facturas_con_errores.
    """
    facturas_correctas = []
    facturas_con_errores = []

    for factura in facturas:
        errores = []

        error = verificar.num_factura(factura)
        errores.append(error) if error else None

        error = verificar.fecha(factura)
        errores.append(error) if error else None

        error = verificar.base_iva(factura)
        errores.append(error) if error else None

        error = verificar.tipo_iva(factura)
        errores.append(error) if error else None

        error = verificar.cuota_iva(factura)
        errores.append(error) if error else None
        if factura["Cuota I.V.A."] == 0.0: 
            factura["% I.V.A."] = 0.0
        
        error = verificar.total_factura(factura)
        errores.append(error) if error else None

        error = verificar.nif(factura)
        errores.append(error) if error else None

        error = verificar.nombre_cliente(factura)
        errores.append(error) if error else None

        error = verificar.calculo_cuota_iva(factura)
        errores.append(error) if error else None

        error = verificar.calculos_totales(factura)
        errores.append(error) if error else None

        if errores:
            factura["Errores"] = ", ".join(errores)
            facturas_con_errores.append(factura)
        else:
            facturas_correctas.append(factura)

    return facturas_correctas, facturas_con_errores