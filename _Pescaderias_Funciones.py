import re
import ft_comunes as ft
import ft_verificadores as verificar

def registros_factura(pagina, empresa):
    datos_factura = {
        "Num. Factura": numero_factura(pagina),
        "Fecha Fact.": fecha(pagina),
        "Fecha Oper.": fecha(pagina),
        "Concepto": 700,
        "Base I.V.A.": base_iva(pagina),
        "% I.V.A.": 0.0,
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

def numero_factura(pagina):
    num_factura = re.search(r"Nº factura\s*(\d+)", pagina)
    return num_factura.group(1) if num_factura else None

def fecha(pagina):
    fecha = re.search(r"Fecha emisión\s*(.*)", pagina)
    if not fecha:
        return None
    fecha = re.sub(r"[,]","/", fecha.group(1))
    fecha = re.sub(r"[-]","", fecha)
    return fecha

def base_iva(pagina):
    base = re.search(r"Base\s*([\d,\.]+)", pagina)
    return base.group(1) if base else None

def cuota_iva(pagina):
    iva = re.search(r"IVA\s*([\d,\.]+)", pagina)
    return iva.group(1) if iva else None

def nif_cliente(pagina, empresa):
    nif_empresa = empresa["nif"][:8] + "-" + empresa["nif"][-1]
    nif = re.search(rf"{nif_empresa}\s*(.+)", pagina)
    if not nif:
        return None
    nif = re.sub(r"[^a-zA-Z0-9]","", nif.group(1)).upper()
    if nif == "X3581661W":
        nif = "X3586116W"
    return nif

def nombre_cliente(pagina, empresa):
    nombre = re.search(rf"{empresa['nombre']}\s*(.+)", pagina)
    if not nombre:
        return None
    nombre = nombre.group(1)
    if nombre[:20] == "Ramírez Sánchez S.L.":
        nombre = "Ramírez Sánchez S.L. 'Rest Refrectorium'"
    elif nombre[:21] == "Luis Gaspar Rodríguez":
        nombre = "Luis Gaspar Rodríguez 'Rest. El Rengue'"
    return nombre

def total_factura(pagina):
    total_match = re.search(r"Total\s*([\d,\.]+)\s*€?", pagina)
    return total_match.group(1) if total_match else None


def comprobar_totales(factura):
    base = factura["Base I.V.A."]
    cuota = factura["Cuota I.V.A."]
    total = factura["Total Factura"]
    if (not (base and cuota and total)):
        return ("Total factura no verificable")

    total_calculado = round(base + cuota, 2)
    if abs(total_calculado - total) > 0.01:
        # return (f"Diferencia en total factura ({total_calculado} != {total})")
        factura["Base I.V.A."] = round(total/1.1, 2)
        factura["Cuota I.V.A."] = round(total-factura["Base I.V.A."], 2)
        factura["Base I.R.P.F."] = factura["Base I.V.A."]
        factura["Base R. Equiv."] = factura["Base I.V.A."]
    return False # No hay errores

def calcular_tipo_iva(factura):
    base = factura["Base I.V.A."]
    cuota = factura["Cuota I.V.A."]
    if not (base and cuota):
        return ("Tipo de IVA no calculable")
    factura["% I.V.A."] = round((cuota/base) * 100.0, 0)
    if factura["% I.V.A."] != 10:
        # return ("% I.V.A. es distinto de 10")
        total = factura["Total Factura"]
        factura["Base I.V.A."] = round(total/1.1, 2)
        factura["Cuota I.V.A."] = round(total-factura["Base I.V.A."], 2)
        factura["Base I.R.P.F."] = factura["Base I.V.A."]
        factura["Base R. Equiv."] = factura["Base I.V.A."]
    return False # No hay errores

def extraer_facturas_del_PDF(path, empresa):
    paginas = ft.extraer_paginas_PDF_tipo_texto(path)

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

        error = verificar.fecha(factura, is_eeuu=True)
        errores.append(error) if error else None

        error = verificar.base_iva(factura)
        errores.append(error) if error else None

        error = verificar.cuota_iva(factura)
        errores.append(error) if error else None
        
        error = verificar.total_factura(factura)
        errores.append(error) if error else None

        error = verificar.nif(factura)
        errores.append(error) if error else None

        error = verificar.nombre_cliente(factura)
        errores.append(error) if error else None

        error = comprobar_totales(factura)
        errores.append(error) if error else None

        error = calcular_tipo_iva(factura)
        errores.append(error) if error else None

        if errores:
            factura["Errores"] = ", ".join(errores)
            facturas_con_errores.append(factura)
        else:
            facturas_correctas.append(factura)

    return facturas_correctas, facturas_con_errores