import re
import ft_comunes as ft
import ft_extraer_paginas

def facturas_del_PDF(path, empresa):
    paginas = ft_extraer_paginas.tipo_texto(path)

    facturas = []
    for pagina in paginas:
        factura = registros_factura(pagina, empresa)
        if factura:
            facturas.append(factura)
    return facturas

def registros_factura(pagina, empresa):
    datos_factura = {
        "Num. Factura": numero_factura(pagina),
        "Fecha Fact.": fecha(pagina),
        "Fecha Oper.": fecha(pagina),
        "Concepto": 700,
        "Base I.V.A.": base_iva(pagina),
        "% I.V.A.": 0,
        "Cuota I.V.A.": cuota_iva(pagina),
        "Base I.R.P.F.": base_iva(pagina),
        "% I.R.P.F.": 0,
        "Cuota I.R.P.F.": 0,
        "Base R. Equiv.": base_iva(pagina),
        "% R. Equiv.": 0,
        "Cuota R. Equiv.": 0,
        "NIF/DNI": nif_cliente(pagina, empresa),
        "Nombre": nombre_cliente(pagina, empresa),
        "Total Factura": total_factura(pagina)
    }
    return datos_factura

def numero_factura(pagina):
    num_factura = re.search(r"Nº factura\s*(\d+)", pagina)
    return num_factura.group(1) if num_factura else 0

def fecha(pagina):
    fecha = re.search(r"Fecha emisión\s*(.*)", pagina)
    return fecha.group(1) if fecha else 0

def base_iva(pagina):
    base = re.search(r"Base\s*([\d,\.]+)", pagina)
    return base.group(1) if base else 0

def cuota_iva(pagina):
    iva = re.search(r"IVA\s*([\d,\.]+)", pagina)
    return iva.group(1) if iva else 0

def nif_cliente(pagina, empresa):
    nif_empresa = empresa["nif"][:8] + "-" + empresa["nif"][-1]
    nif = re.search(rf"{nif_empresa}\s*(.+)", pagina)
    return nif.group(1) if nif else 0

def nombre_cliente(pagina, empresa):
    nombre = re.search(rf"{empresa['nombre']}\s*(.+)", pagina)
    return nombre.group(1) if nombre else 0

def total_factura(pagina):
    total_match = re.search(r"Total\s*([\d,\.]+)\s*€?", pagina)
    return total_match.group(1) if total_match else 0